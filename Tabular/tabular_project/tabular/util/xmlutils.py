import os
from rich.console import Console 
from ..data.account_config import AccountConfig
from ..data.money import Money
from ..data.backend import Backend

import xml.etree.ElementTree as ET

console = Console()

def load_xml_config(file_path) -> list[AccountConfig]:
    """Load and parse the XML configuration file."""
    if not os.path.exists(file_path):
        console.print(f"❌ Error: File '{file_path}' does not exist.", style="bold red")
        return None
    if not file_path.endswith(".xml"):
        console.print(f"❌ Error: File '{file_path}' is not an XML file.", style="bold red")
        return None

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check if the root tag is 'accounts'
        if root.tag != 'accounts':
            console.print(f"❌ Error: Root tag is '{root.tag}', expected 'accounts'.", style="bold red")
            return None
        # Check if there are any 'account' elements
        accountXml = root.findall('account')
        if not accountXml:
            console.print(f"❌ Error: No 'account' elements found.", style="bold red")
            return None
        
        accountConfigs: list[AccountConfig] = []
        for property in accountXml:
            id = property.get('id')
            type = property.findtext('type')
            description = property.findtext('description')
            path = property.findtext('path')

            moneyXml = property.find('money')
            if moneyXml is not None:
                base = moneyXml.findtext('base')
                currency = moneyXml.findtext('currency')
                risk = moneyXml.findtext('risk')
            else:
                base = None
                currency = None
                risk = None
            
            backendXml = property.find('backend')
            if backendXml is not None:
                firm = backendXml.findtext('firm')
                server = backendXml.findtext('server')
                url = backendXml.findtext('url')
            else:
                base = None
                currency = None
                url = None

            accountConfig = AccountConfig(
                id=id,
                type=type,
                description=description,
                path=path,
                money=Money(base=base, currency=currency, risk=risk),
                backend=Backend(firm=firm, server=server, urlToServer=url)
            )
            accountConfigs.append(accountConfig)

        return accountConfigs
    except ET.ParseError as e:
        console.print(f"❌ Error parsing XML file: {e}", style="bold red")
        return None