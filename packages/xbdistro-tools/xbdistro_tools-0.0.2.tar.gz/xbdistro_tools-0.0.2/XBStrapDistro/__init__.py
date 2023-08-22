import os
from pprint import pprint
from dataclasses import dataclass

import yaml
from yaml.loader import SafeLoader


@dataclass
class Metadata:
    categories: []
    line: str = ""
    summary: str = ""
    description: str = ""
    website: str = ""
    maintainer: str = ""
    spdx: str = ""

    def __init__(self, metadata_data):
        self.categories = []
        if metadata_data is None:
            return
        self.line = metadata_data["__line__"]
        if "summary" in metadata_data:
            self.summary = metadata_data["summary"]
        if "description" in metadata_data:
            self.description = metadata_data["description"]
        if "website" in metadata_data:
            self.website = metadata_data["website"]
        if "maintainer" in metadata_data:
            self.maintainer = metadata_data["maintainer"]
        if "categories" in metadata_data:
            self.categories = metadata_data["categories"]
        if "spdx" in metadata_data:
            self.spdx = metadata_data["spdx"]


@dataclass
class Source:
    name: str
    file: str
    line: str
    sources_required: []
    tools_required: []
    regenerate: []
    version: str = "unknown"
    subdir: str = ""
    url: str = ""
    checksum: str = ""
    extract_path: str = ""
    type: str = "unknown"
    tag: str = ""
    branch: str = ""
    commit: str = ""

    def __init__(self, source_data, filename, name=None):
        self.sources_required = []
        self.tools_required = []
        self.regenerate = []
        self.line = source_data["__line__"]
        self.file = filename
        if name is not None:
            self.name = name
        else:
            assert "name" in source_data
            self.name = source_data["name"]
        if "subdir" in source_data:
            self.subdir = source_data["subdir"]
        if "url" in source_data:
            if "format" in source_data:
                self.type = source_data["format"] + "_"
            else:
                self.type = ""
            self.type = self.type + "file"
            self.url = source_data["url"]
        elif "git" in source_data:
            self.type = "git_repository"
            self.url = source_data["git"]
        elif "svn" in source_data:
            self.type = "subversion_repository"
            self.url = source_data["svn"]
        elif "hg" in source_data:
            self.type = "hg_repository"
            self.url = source_data["hg"]
        elif self.subdir == "meta-sources":
            self.type = "metasource"
        if "extract_path" in source_data:
            self.extract_path = source_data["extract_path"]
        if "version" in source_data:
            self.version = source_data["version"]
        if "sources_required" in source_data:
            self.sources_required = source_data["sources_required"]
            if self.type == "unknown":
                self.type = "metasource"
        if "tools_required" in source_data:
            self.tools_required = source_data["tools_required"]
        if "regenerate" in source_data:
            self.regenerate = source_data["regenerate"]
        if "tag" in source_data:
            self.tag = source_data["tag"]
        if "branch" in source_data:
            self.branch = source_data["branch"]
        if "commit" in source_data:
            self.commit = source_data["commit"]
        if self.type == "unknown":
            print(" --- ERROR ---\n  unknown source type!")
            pprint(source_data)
            assert False


@dataclass
class Package:
    name: str
    source: Source
    metadata: Metadata
    labels: []
    dependencies: []
    tools_required: []
    configure: []
    build: []
    revision: int = 1
    architecture: str = ""
    line: str = ""
    file: str = ""
    from_source: str = ""
    stability_level: str = "okay"

    def __init__(self, package_data, filename):
        self.file = filename
        self.line = package_data["__line__"]
        self.labels = []
        self.dependencies = []
        self.tools_required = []
        self.configure = []
        self.build = []
        # Basic package metadata
        if "name" in package_data:
            self.name = package_data["name"]
        if "pkgs_required" in package_data:
            self.dependencies = package_data["pkgs_required"]
        else:
            self.dependencies = []
        if "revision" in package_data:
            self.revision = package_data["revision"]
        if "stability_level" in package_data:
            self.stability_level = package_data["stability_level"]
        if "labels" in package_data:
            self.labels = package_data["labels"]
        if "architecture" in package_data:
            self.architecture = package_data["architecture"]

        # Package buiöd
        if "tools_required" in package_data:
            self.tools_required = package_data["tools_required"]
        if "configure" in package_data:
            self.configure = package_data["configure"]
        if "build" in package_data:
            self.build = package_data["build"]

        # More package metadata
        if "metadata" in package_data:
            self.metadata = Metadata(package_data["metadata"])
        else:
            self.metadata = Metadata(None)

        # Package source
        if "source" in package_data:
            self.source = Source(package_data["source"], filename, self.name + "__embedded_source")
        elif "from_source" in package_data:
            self.from_source = package_data["from_source"]
            self.source = None


class XBStrapDistro:
    class SafeLineLoader(SafeLoader):
        def construct_mapping(self, node, deep=False):
            mapping = super(XBStrapDistro.SafeLineLoader, self).construct_mapping(node, deep=deep)
            # Add 1 so line numbering starts at 1
            mapping['__line__'] = node.start_mark.line + 1
            return mapping

    # TODO: better line number storage

    __repo_dir = ""

    __global_sources: list[Source] = []
    __packages: list[Package] = []

    @property
    def global_sources(self):
        return self.__global_sources

    @property
    def packages(self):
        return self.__packages

    def find_source_by_name(self, name) -> Source | None:
        for source in self.__global_sources:
            if source.name == name:
                return source
        return None

    def find_package_by_name(self, name) -> Package | None:
        for package in self.__packages:
            if package.name == name:
                return package
        return None

    def import_global_sources(self, file_path):
        data = None
        with open(os.path.join(self.__repo_dir, file_path), "r") as stream:
            try:
                data = yaml.load(stream, Loader=self.SafeLineLoader)
            except yaml.YAMLError as exc:
                print(exc)
                return

        if "imports" in data:
            for file_import in data["imports"]:
                self.import_global_sources(file_import["file"])

        if "sources" in data:
            for source_data in data["sources"]:
                self.__global_sources.append(Source(source_data, file_path))

    def import_packages(self, file_path):
        data = None
        with open(os.path.join(self.__repo_dir, file_path), "r") as stream:
            try:
                data = yaml.load(stream, Loader=self.SafeLineLoader)
            except yaml.YAMLError as exc:
                print(exc)
                return

        if "imports" in data:
            for file_import in data["imports"]:
                self.import_packages(file_import["file"])

        if "packages" in data:
            for package_data in data["packages"]:
                package = Package(package_data, file_path)
                if package.from_source != "":
                    package.source = self.find_source_by_name(package.from_source)
                assert package.source is not None
                self.__packages.append(package)

    def get_package_names(self) -> list[str]:
        ret: list[str] = []
        for package in self.__packages:
            ret.append(package.name)
        return ret

    def __init__(self, folder):
        self.__repo_dir = folder
