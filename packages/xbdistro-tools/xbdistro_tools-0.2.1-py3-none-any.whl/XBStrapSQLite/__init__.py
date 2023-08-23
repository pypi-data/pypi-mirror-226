import sqlite3
from dataclasses import dataclass
from XBStrapDistro import XBStrapDistro, Package, Source


@dataclass
class XBStrapSQLiteChangeReport:
    packages: [Package]
    sources: [Source]

    package_change: [str]
    package_changed_source: [str]
    new_packages: [str]

    def get_package_change_reason(self, package_name: str):
        ret = ""
        package_changed: bool = package_name in self.package_change
        package_source_changed: bool = package_name in self.package_changed_source
        package_new: bool = package_name in self.new_packages
        if package_new:
            ret = "New package"
        elif package_changed and package_source_changed:
            ret = "Recipe changed, Source changed"
        else:
            if package_changed:
                ret = "Recipe changed"
            elif package_source_changed:
                ret = "Source changed"
        return ret

    def __init__(self):
        self.packages = []
        self.sources = []
        self.package_change = []
        self.package_changed_source = []
        self.new_packages = []


def update_source_dependencies(c: sqlite3.Cursor, source: Source, change_report: XBStrapSQLiteChangeReport):
    data = []
    for dependency in source.sources_required:
        if type(dependency) is dict:
            is_recursive: bool = False
            if "recursive" in dependency:
                is_recursive = dependency["recursive"]
            data.append((source.name, dependency["name"], is_recursive))
        elif type(dependency) is str:
            data.append((source.name, dependency, False))
        else:
            assert False

    dependencies_in_database = c.execute("SELECT source_name, source_depend, is_recursive FROM source_dependencies"
                                         " WHERE source_name = '{}'"
                                         .format(source.name)).fetchall()

    missing_dependencies = [x for x in data if x not in dependencies_in_database]
    dependencies_to_delete = [x for x in dependencies_in_database if x not in data]
    if len(missing_dependencies):
        c.executemany("INSERT INTO source_dependencies(source_name, source_depend, is_recursive) VALUES(?, ?, ?)",
                      missing_dependencies)
    if len(dependencies_to_delete):
        for dependency in dependencies_to_delete:
            c.execute("DELETE FROM source_dependencies WHERE source_name='{}' AND source_depend='{}'"
                      .format(dependency[0], dependency[1]))


def update_package_dependencies(c: sqlite3.Cursor, package: Package, change_report: XBStrapSQLiteChangeReport):
    data = []
    for dependency in package.dependencies:
        data.append((package.name, dependency))

    dependencies_in_database = c.execute("SELECT package_name, package_depend FROM package_dependencies"
                                         " WHERE package_name = '{}'"
                                         .format(package.name)).fetchall()

    missing_dependencies = [x for x in data if x not in dependencies_in_database]
    dependencies_to_delete = [x for x in dependencies_in_database if x not in data]
    if len(missing_dependencies):
        c.executemany("INSERT INTO package_dependencies(package_name, package_depend) VALUES(?, ?)",
                      missing_dependencies)
    if len(dependencies_to_delete):
        for dependency in dependencies_to_delete:
            print(dependency)
            c.execute("DELETE FROM package_dependencies WHERE package_name='{}' AND package_depend='{}'"
                      .format(dependency[0], dependency[1]))


def update_source_in_database(c: sqlite3.Cursor, source: Source, change_report: XBStrapSQLiteChangeReport) -> bool:
    # Check if row exists
    c.execute("SELECT EXISTS (SELECT 1 FROM sources WHERE source_name='{}' LIMIT 1)".format(source.name))
    if not c.fetchone()[0]:
        change_report.sources.append(source)
        c.execute("INSERT INTO sources(source_name, type, version) VALUES('{}', '{}', '{}')"
                  .format(source.name, source.type, source.version))
        return True
    else:
        c.execute(
            "UPDATE sources SET type='{}', version='{}' WHERE source_name='{}' AND NOT (version='{}' AND type='{}')"
            .format(source.type, source.version, source.name, source.version, source.type))
        if c.rowcount == 1:
            change_report.sources.append(source)
            return True
    return False


def update_package_in_database(c: sqlite3.Cursor, package: Package, change_report: XBStrapSQLiteChangeReport):
    # Check if row exists
    c.execute("SELECT EXISTS (SELECT 1 FROM packages WHERE name='{}' LIMIT 1)".format(package.name))
    if not c.fetchone()[0]:
        c.execute("INSERT OR REPLACE INTO packages(name, source_name, revision, maintainer) VALUES('{}', '{}', {}, '{}')"
                  .format(package.name, package.source.name, package.revision, package.metadata.maintainer))
        change_report.packages.append(package)
        change_report.new_packages.append(package)
    else:
        c.execute(
            "UPDATE packages SET source_name='{}', revision='{}', maintainer='{}' WHERE name='{}' AND NOT (source_name='{}' AND revision='{}' AND maintainer='{}')"
            .format(package.source.name, package.revision, package.metadata.maintainer, package.name, package.source.name, package.revision, package.metadata.maintainer))
        if c.rowcount == 1:
            change_report.packages.append(package)
            change_report.package_change.append(package.name)
    if "__embedded_source" in package.source.name:
        if update_source_in_database(c, package.source, change_report):
            if package not in change_report.packages:
                change_report.packages.append(package)
            change_report.package_changed_source.append(package.name)


class XBStrapSQLite:
    distro: XBStrapDistro

    def __initialize_database(self):
        c = self.database.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS packages(name CHAR PRIMARY KEY, source_name CHAR, revision INT, maintainer CHAR)")
        c.execute("CREATE TABLE IF NOT EXISTS package_dependencies(package_name CHAR, package_depend CHAR)")
        c.execute(
            "CREATE TABLE IF NOT EXISTS source_dependencies(source_name CHAR, source_depend CHAR, is_recursive BOOL)")
        c.execute("CREATE TABLE IF NOT EXISTS file_lines(package_name CHAR, entry CHAR, file CHAR, line INT)")
        c.execute("CREATE TABLE IF NOT EXISTS sources(source_name CHAR PRIMARY KEY, type CHAR, version CHAR)")

    def __update_global_sources_in_database(self, change_report: XBStrapSQLiteChangeReport):
        c = self.database.cursor()
        for source in self.distro.global_sources:
            update_source_in_database(c, source, change_report)
        self.database.commit()

    def __update_packages_in_database(self, change_report: XBStrapSQLiteChangeReport):
        c = self.database.cursor()
        for package in self.distro.packages:
            update_package_in_database(c, package, change_report)
        self.database.commit()

    def __update_package_dependencies_in_database(self, change_report: XBStrapSQLiteChangeReport):
        c = self.database.cursor()
        for package in self.distro.packages:
            update_package_dependencies(c, package, change_report)
        self.database.commit()

    def __update_source_dependencies_in_database(self, change_report: XBStrapSQLiteChangeReport):
        c = self.database.cursor()
        for source in self.distro.global_sources:
            update_source_dependencies(c, source, change_report)
        for package in self.distro.packages:
            if package.source not in self.distro.global_sources:
                update_source_dependencies(c, package.source, change_report)
        self.database.commit()

    # We do not store any changes about this in the change report, as these may change often
    # We also just truncate the table first, as its not worth trying to optimize whether to insert something or not
    def __update_filelines_in_database(self):
        c = self.database.cursor()
        c.execute("DELETE FROM file_lines")
        for package in self.distro.packages:
            c.execute("INSERT INTO file_lines(package_name, entry, file, line) VALUES(?, ?, ?, ?)",
                      [package.name, "main_def", package.file, package.line])
            # The metadata can only be defined inline, so we use the file that the package is defined in
            c.execute("INSERT INTO file_lines(package_name, entry, file, line) VALUES(?, ?, ?, ?)",
                      [package.name, "meta_def", package.file, package.metadata.line])
            # We reuse the package_name for the source as well
            # Check if row exists
            c.execute("SELECT EXISTS (SELECT 1 FROM file_lines WHERE package_name = ? AND entry='source_def' LIMIT 1)",
                      ["__source__" + package.source.name])
            if not c.fetchone()[0]:
                c.execute("REPLACE INTO file_lines(package_name, entry, file, line) VALUES(?, ?, ?, ?)",
                          ["__source__" + package.source.name, "source_def", package.source.file, package.source.line])
        self.database.commit()

    def update_database(self):
        change_report = XBStrapSQLiteChangeReport()
        print("--- Beginning database update ---")
        print("Updating global sources")
        self.__update_global_sources_in_database(change_report)
        print("Updating packages")
        self.__update_packages_in_database(change_report)
        print("Updating package dependencies")
        self.__update_package_dependencies_in_database(change_report)
        print("Updating source dependencies")
        self.__update_source_dependencies_in_database(change_report)
        print("Updating file lines")
        self.__update_filelines_in_database()
        print("--- Done doing database update ---")
        return change_report

    def __init__(self, _distro: XBStrapDistro, sql_lite_file):
        self.distro = _distro
        self.database = sqlite3.connect(sql_lite_file)
        assert self.database is not None
        self.__initialize_database()
