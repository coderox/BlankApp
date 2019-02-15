import argparse
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='inject_nuget_xml')
parser.add_argument('path')
parser.add_argument('project_name')

args = parser.parse_args()

def fix_project_file(file, cppwinrt_version):
    ET.register_namespace("", "http://schemas.microsoft.com/developer/msbuild/2003")
    tree = ET.parse(file)
    root = tree.getroot()

    # Remove MIDL section (which will be populated by nuget package props)
    for definition in root.iter('{http://schemas.microsoft.com/developer/msbuild/2003}ItemDefinitionGroup'):
        for midl in definition.iter('{http://schemas.microsoft.com/developer/msbuild/2003}Midl'):
            definition.remove(midl)

    # Add DependentUpon if .xaml file exists, leveraged by C++/WinRT metadata generation
    for item_group in root.iter('{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup'):
        for included_file in item_group.iter('{http://schemas.microsoft.com/developer/msbuild/2003}ClInclude'):
            xaml_file = included_file.attrib['Include'].replace('.h', '.xaml')
            if os.path.isfile(xaml_file):
                dependency = ET.SubElement(included_file, "DependentUpon")
                dependency.text = xaml_file

    package = "packages\\Microsoft.Windows.CppWinRT." + cppwinrt_version + "\\build\\native\\Microsoft.Windows.CppWinRT"
    props =  package + ".props"
    target = package + ".targets"

    #   <Import Project="<package>.props" 
    #           Condition="Exists('<package>.props')" />
    import_element = ET.SubElement(root, "Import")
    import_element.attrib['Project'] = props
    import_element.attrib['Condition'] = "Exists('" + props + "')"

    # <ImportGroup Label="PropertySheets">
    #     <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props"
    #             Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')"
    #             Label="LocalAppDataPlatform" />
    #     <Import Project="<package>.targets" 
    #             Condition="Exists('<package>.targets')" />
    # </ImportGroup>
    import_group_element = ET.SubElement(root, "ImportGroup")
    import_group_element.attrib['Label'] = "PropertySheets"

    import_element_one = ET.SubElement(import_group_element, "Import")
    import_element_one.attrib['Project'] = "$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props"
    import_element_one.attrib['Condition'] = "exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')"
    import_element_one.attrib['Label'] = "LocalAppDataPlatform"

    import_element_two = ET.SubElement(import_group_element, "Import")
    import_element_two.attrib['Project'] = target
    import_element_two.attrib['Condition'] = "Exists('" + target + "')"

    tree.write(file, xml_declaration=True, encoding='utf-8')

def find_cppwinrt_version(file):
    tree = ET.parse(file)
    root = tree.getroot()
    for packages in root.iter('packages'):
        for package in packages.iter('package'):
            if(package.attrib['id'] == 'Microsoft.Windows.CppWinRT'):
                return package.attrib['version']

version = find_cppwinrt_version(args.path + '\packages.config')
project_file = args.path + args.project_name + '.vcxproj'

fix_project_file(project_file, version)