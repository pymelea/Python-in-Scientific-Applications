from asyncio import Semaphore, gather, run, wait_for
from aiohttp.client import ClientSession
from sys import argv, stderr
from os import path
import aiofiles
import json


# Function to async download file from url
async def download_file(url, session, sem, dest_file):
    async with sem:
        print(f'Downloading {url}')
        async with session.get(url) as res:
            content = await res.read()

        # Check everything went well
        if res.status != 200:
            print(f'Download failed: {res.status}')
            return

        async with aiofiles.open(dest_file, '+wb') as f:
            await f.write(content)
            

# Function to async download several files 
async def download_several_files(urls: list, time: int, tasks: int):
    tasks_list = []
    sem = Semaphore(tasks)

    async with ClientSession() as session:
        for url in urls:
            # assumes that the last segment after the / represents the file name
            # if url is abc/xyz/file.txt, the file name will be file.txt
            file_name_start_pos = url.rfind("/") + 1
            file_name = url[file_name_start_pos:]
            dest_file = f'file_{file_name}.pdf'
            tasks_list.append(wait_for(download_file(url, session, sem, dest_file), timeout = time))

        return await gather(*tasks_list)


if __name__ == '__main__':

    # simple protection
    try:
        filename = argv[1]
        time = int(argv[2])
        tasks = int(argv[3])
    except IndexError:
        print(f'Usage: {path.basename(__file__)} <filename.json> <time> <tasks>')
        exit(1)
    
    if not path.exists(filename):
        print(f'No such file "{filename}"', file = stderr)
        exit(2)

    with open(filename, 'r', encoding = 'utf-8') as json_file:
        files = json.load(json_file)

    run(download_several_files(files, time, tasks))
