"""OdsCharList - Class for OpenDocument xml characters table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ods.ods_builder import OdsBuilder
from pywriter.ods.ods_file import OdsFile


class OdsCharList(OdsFile):
    """OpenDocument xml characters spreadsheet representation.
    """

    DESCRIPTION = 'Character list'
    SUFFIX = '_charlist'

    fileHeader = OdsBuilder.CONTENT_XML_HEADER + DESCRIPTION + '''" table:style-name="ta1" table:print="false">
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:number-columns-repeated="3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:number-columns-repeated="1014" table:default-cell-style-name="Default"/>
     <table:table-row table:style-name="ro1">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Name</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Full name</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Aka</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Description</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Bio</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Goals</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Importance</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Tags</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Notes</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1014"/>
    </table:table-row>

'''

    characterTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell office:value-type="string">
      <text:p>CrID:$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$FullName</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$AKA</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Bio</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Goals</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Status</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Tags</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell table:number-columns-repeated="1014"/>
    </table:table-row>

'''

    fileFooter = OdsBuilder.CONTENT_XML_FOOTER