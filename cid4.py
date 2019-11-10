#
#   Ramil Salayev
#


import sys
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from subprocess import call
from os import chdir
call('', shell=True)


class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def control_cc_list(sysa):
    if (sysa + ' ') in comics_company_list:
        return True
    else:
        return False


def main(sys_argv_1, sys_argv_2, sys_argv_3, comic_name_list, comic_link_list):
    global mydivs

    url = 'https://freshcomics.us/issues/'+sys_argv_1
    print(bcolor.BOLD + bcolor.WARNING + 'Main URL:', url + bcolor.ENDC)
    print(100*'=')
    main_r = requests.get(url)
    soup = BeautifulSoup(main_r.text, 'html.parser')
    mydivs = soup.findAll('div', class_='section')
    get_comics_company_name()
    if control_cc_list(sysa=sys.argv[3]):
        print(bcolor.OKBLUE + "True" + bcolor.ENDC)
        for div in mydivs:  # lets take all divs in site.
            # There are "header" in div,we have to get them.
            for h2 in div.find_all('h2', class_='entry-title'):
                if sys_argv_3 in h2.contents[0]:
                    for row in div.find_all('div', class_='row'):
                        for row_div in row.find_all('div', class_='col-sm-3'):
                            # print(row_div.find('div').find('a').get('href'))
                            # print(row_div.find('div').find('a').contents[0])

                            # You can type "row_div.find('div').find('a').text" like this.
                            comic_name = row_div.find(
                                'div').find('a').contents[0]
                            comics_link = 'https://freshcomics.us' + \
                                row_div.find('div').find('a').get('href')
                            # append them to their own list.
                            comic_name_list.append(comic_name)
                            comic_link_list.append(comics_link)
                        break

    else:
        print(bcolor.FAIL + "Something going wrong" + bcolor.ENDC)


def get_comics_company_name():
    global comics_company_list
    comics_company_list = []
    for div in mydivs:
        for h2 in div.find_all('h2', class_=('entry-title')):
            if h2.contents[0].split('\n')[1].split('\t')[-1] in comics_company_list:
                pass
            else:
                comics_company_list.append(
                    h2.contents[0].split('\n')[1].split('\t')[-1])


def function_of_comic_book_link(link_list, name_list):
    global image_link_for_download

    image_link_for_download = []
    count_for_number = 1
    for link in link_list:
        r_2 = requests.get(link)

        print('Status code:', bcolor.OKGREEN +
              str(r_2.status_code) + ' -->> OK'+bcolor.ENDC+'\t\t\t\tImage number:', count_for_number)
        print('URL of comic book:', bcolor.OKBLUE + r_2.url + bcolor.ENDC)
        soup = BeautifulSoup(r_2.text, 'html.parser')
        mydivs = soup.findAll('div', class_='section')
        for mydiv in mydivs:
            comic_name = mydiv.find('h2').contents[0].split()
            print('Comic Name:', end=' ')
            for i in comic_name:
                print(i, end=' ')
            for image in mydiv.find_all('div', class_='cover-image'):
                image_link = image.find('a').get('href')
                print('\nImage link: {:<50}'.format(
                    bcolor.WARNING + image_link + bcolor.ENDC))
                count_for_number += 1
                image_link_for_download.append(image_link)
                print(80*'-'+'\n')

    input(str(count_for_number-1) +
          ' Image can be download\nPress enter to download\n')


def function_of_download_image(links, sys_argv):
    # You can download image with urllib module,urllib.request.urlretrive('<Image link>', '<image name>')
    count_for_number = 1
    for url in links:
        r = requests.get(url)
        image = Image.open(BytesIO(r.content))
        directory = sys_argv
        image_name = url.split('/')[-1]
        with open(directory+image_name, 'wb') as f:
            f.write(r.content)
        print(bcolor.OKBLUE + 'Image name: {}\t'.format(image_name) + "  Image Size: {}\tImage format: {}".format(image.size,
                                                                                                                  image.format) + bcolor.ENDC, bcolor.OKGREEN + "\n\nSuccessfully Downloaded" + bcolor.ENDC, '\t\t\tImage number:', count_for_number)
        count_for_number += 1
        print(80*'-')


help_list = ['help', '--help', 'h', '-h']
try:
    if sys.argv[1] in help_list:
        print('\nDownload any comics images from fresh comics.\nUse:\n<scrip_name> <YYYY-MM-DD> <Download Directory> <"Comics Company">')
    elif sys.argv[2] == '--list' or sys.argv[1] == '-l':
        url = 'https://freshcomics.us/issues/' + sys.argv[1]
        print(bcolor.BOLD + bcolor.WARNING + 'Main URL:', url + bcolor.ENDC)
        print(100*'=')
        main_r = requests.get(url)
        soup = BeautifulSoup(main_r.text, 'html.parser')
        mydivs = soup.findAll('div', class_='section')
        for div in mydivs:
            for h2 in div.find_all('h2', class_=('entry-title')):
                print("{:<25}{:>18}".format(h2.contents[0].split('\n')[1].split(
                    '\t')[-1], h2.contents[0].split('\n')[3].split(
                    '\t')[-1]))

    elif len(sys.argv) > 4:
        pass
    else:
        chdir(str(sys.argv[2]))
        comic_name_list = []
        comic_link_list = []
        main(sys.argv[1], sys.argv[2], sys.argv[3],
             comic_name_list, comic_link_list)
        function_of_comic_book_link(comic_link_list, comic_name_list)
        function_of_download_image(image_link_for_download, sys.argv[2])
except IndexError:
    print(bcolor.WARNING + '\nYou can see how to use cid4 with "cid4 -h"'+bcolor.ENDC)
except FileNotFoundError:
    print(bcolor.FAIL + '\n[-] Directory is not exist'+bcolor.ENDC)
