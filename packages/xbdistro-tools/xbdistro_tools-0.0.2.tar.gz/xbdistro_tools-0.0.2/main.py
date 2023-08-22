from git import Repo
import os
from XBStrapDistro import XBStrapDistro, Package, Source
from XBStrapSQLite import XBStrapSQLite
from pprint import pprint
import _thread
import PySimpleGUI as sg

repo_url = "https://github.com/managarm/bootstrap-managarm.git"
repo_dir = "boostrap-managarm"
distro = XBStrapDistro(repo_dir)
sqlite_database = XBStrapSQLite(distro, "packages.db")

# Main window
package_selector_column = [
    [sg.Text("XBStrap Distro Editor")],
    [sg.Listbox(values=[], key="__PACKAGE_LIST__", expand_y=True)]
]

package_info_column = [
    [sg.Text("Select Package", key="__PACKAGE_NAME__")]
]

main_window_layout = [
    [sg.Column(package_selector_column, expand_y=True),
     sg.VSeperator(),
     sg.Column(package_info_column, expand_y=True, expand_x=True)
     ]
]
main_window: sg.Window

loading_screen_layout = [
    [sg.Text("Loading...")],
    [sg.ProgressBar(100, key="__PROGRESS__", expand_x=True)]
]
loading_screen_window: sg.Window


def update_git_repo():
    if os.path.exists(os.path.join(repo_dir, ".git")):
        repo = Repo(repo_dir)
        assert not repo.bare
        # origin = repo.remotes.origin
        # origin.pull()
    else:
        repo = Repo.clone_from(repo_url, repo_dir)
        assert not repo.bare


def open_loading_window():
    global loading_screen_window
    loading_screen_window = sg.Window("Loading", loading_screen_layout)


init_status = 0


def perform_init():
    global init_status
    print("Initializing git repository")
    update_git_repo()
    init_status = 1
    print("Reading global sources")
    distro.import_global_sources("bootstrap.yml")
    init_status = 2
    print("Reading packages")
    distro.import_packages("bootstrap.yml")
    init_status = 3
    sqlite_database.update_database()
    init_status = 4


def main():
    global loading_screen_window
    global init_status
    global main_window

    perform_init()

    # Open main window
    main_window = sg.Window("XBStrap Distro Editor", main_window_layout, resizable=True, location=(100, 100), size=(400, 400), finalize=True)
    # Fill package list
    main_window["__PACKAGE_LIST__"].update(values=distro.get_package_names())
    while True:
        event, values = main_window.read()
        print(event, values)
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

    main_window.close()


if __name__ == '__main__':
    main()
