import re


def winunattend(mac):
	# L'adresse MAC doit être en majuscule et séparée par des "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par "-"
	mac = "-".join(listmac)
	# On met en majuscule
	mac = mac.upper()
	# fichier de sortie
	file = '/samba/winserv2016/' + mac + '.xml'
	
	
	# variables
	productkey = 'WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY'
	computername = 'TestComputerName'
	mdp_admin = 'password'
	regorg = 'castleit'
	regown = 'castleit'
	
	
	with open(file , 'w') as fichier:	
		fichier.write('<?xml version="1.0" encoding="utf-8"?> \n')
		fichier.write('<unattend xmlns="urn:schemas-microsoft-com:unattend"> \n')
		fichier.write('    <settings pass="specialize"> \n')
		fichier.write('        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <AutoLogon> \n')
		fichier.write('                <Password> \n')
		fichier.write('                    <Value>{}</Value> \n'.format(mdp_admin))
		fichier.write('                    <PlainText>true</PlainText> \n')
		fichier.write('                </Password> \n')
		fichier.write('                <Enabled>true</Enabled> \n')
		fichier.write('                <Username>Administrateur</Username> \n')
		fichier.write('                <LogonCount>1</LogonCount> \n')
		fichier.write('            </AutoLogon> \n')
		fichier.write('            <ComputerName>{}</ComputerName> \n'.format(computername))
		fichier.write('            <RegisteredOrganization>{}</RegisteredOrganization> \n'.format(regorg))
		fichier.write('            <RegisteredOwner>{}</RegisteredOwner> \n'.format(regown))
		fichier.write('            <TimeZone>Romance Standard Time</TimeZone> \n')
		fichier.write('        </component>		 \n')
		fichier.write('    </settings> \n')
		fichier.write('    <settings pass="oobeSystem"> \n')
		fichier.write('        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <FirstLogonCommands> \n')
		fichier.write('                <SynchronousCommand wcm:action="add"> \n')
		fichier.write('                    <CommandLine>PowerShell -Command "New-NetLbfoTeam -Name 'bond0' -TeamMembers 'Ethernet','Ethernet 2' -TeamingMode SwitchIndependent -LoadBalancingAlgorithm TransportPorts -Confirm:$false"</CommandLine> \n')
		fichier.write('                    <Description>Active le teaming</Description> \n')
		fichier.write('                    <Order>1</Order> \n')
		fichier.write('                </SynchronousCommand> \n')
		fichier.write('                <SynchronousCommand wcm:action="add"> \n')
		fichier.write('                    <CommandLine>net use N: \\10.10.75.2\public /user:user pass</CommandLine> \n')
		fichier.write('                    <Description>Mappe le lecteur</Description> \n')
		fichier.write('                    <Order>2</Order> \n')
		fichier.write('                </SynchronousCommand> \n')
		fichier.write('                <SynchronousCommand wcm:action="add"> \n')
		fichier.write('                    <CommandLine>diskpart.exe /s N:\winserv2016\MirrorDiskpart.txt</CommandLine> \n')
		fichier.write('                    <Description>Crée un miroir</Description> \n')
		fichier.write('                    <Order>3</Order> \n')
		fichier.write('                </SynchronousCommand> \n')
		fichier.write('                <SynchronousCommand wcm:action="add"> \n')
		fichier.write('                    <CommandLine>net use N: /delete</CommandLine> \n')
		fichier.write('                    <Description>Supprimer le mappage</Description> \n')
		fichier.write('                    <Order>4</Order> \n')
		fichier.write('                </SynchronousCommand>				 \n')
		fichier.write('            </FirstLogonCommands>             \n')
		fichier.write('			<OOBE> \n')
		fichier.write('                <HideEULAPage>true</HideEULAPage> \n')
		fichier.write('                <HideLocalAccountScreen>true</HideLocalAccountScreen> \n')
		fichier.write('                <HideOnlineAccountScreens>true</HideOnlineAccountScreens> \n')
		fichier.write('				<NetworkLocation>Work</NetworkLocation> \n')
		fichier.write('                <ProtectYourPC>1</ProtectYourPC> \n')
		fichier.write('				<SkipMachineOOBE>true</SkipMachineOOBE> \n')
		fichier.write('                <SkipUserOOBE>true</SkipUserOOBE> \n')
		fichier.write('            </OOBE> \n')
		fichier.write('            <UserAccounts> \n')
		fichier.write('                <AdministratorPassword> \n')
		fichier.write('                    <Value>{}</Value> \n'.format(mdp_admin))
		fichier.write('                    <PlainText>true</PlainText> \n')
		fichier.write('                </AdministratorPassword> \n')
		fichier.write('            </UserAccounts> \n')
		fichier.write('        </component> \n')
		fichier.write('    </settings> \n')
		fichier.write('    <settings pass="windowsPE"> \n')
		fichier.write('        <component name="Microsoft-Windows-International-Core-WinPE" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <SetupUILanguage> \n')
		fichier.write('                <UILanguage>fr-FR</UILanguage> \n')
		fichier.write('            </SetupUILanguage> \n')
		fichier.write('            <InputLocale>fr-FR</InputLocale> \n')
		fichier.write('            <SystemLocale>fr-FR</SystemLocale> \n')
		fichier.write('            <UILanguage>fr-FR</UILanguage> \n')
		fichier.write('            <UILanguageFallback>fr-FR</UILanguageFallback> \n')
		fichier.write('            <UserLocale>fr-FR</UserLocale> \n')
		fichier.write('        </component>	 \n')
		fichier.write('        <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <DiskConfiguration> \n')
		fichier.write('			  <Disk wcm:action="add"> \n')
		fichier.write('				<DiskID>0</DiskID>  \n')
		fichier.write('				<WillWipeDisk>true</WillWipeDisk>  \n')
		fichier.write('				<CreatePartitions> \n')
		fichier.write('				  <!-- System partition --> \n')
		fichier.write('				  <CreatePartition wcm:action="add"> \n')
		fichier.write('					<Order>1</Order>  \n')
		fichier.write('					<Type>Primary</Type>  \n')
		fichier.write('					<Size>350</Size>  \n')
		fichier.write('				  </CreatePartition> \n')
		fichier.write('				  <!-- Windows partition --> \n')
		fichier.write('				  <CreatePartition wcm:action="add"> \n')
		fichier.write('					<Order>2</Order>  \n')
		fichier.write('					<Type>Primary</Type>  \n')
		fichier.write('					<Extend>true</Extend>  \n')
		fichier.write('				  </CreatePartition> \n')
		fichier.write('				</CreatePartitions> \n')
		fichier.write('				<ModifyPartitions> \n')
		fichier.write('				  <!-- System partition --> \n')
		fichier.write('				  <ModifyPartition wcm:action="add"> \n')
		fichier.write('					<Order>1</Order>  \n')
		fichier.write('					<PartitionID>1</PartitionID>  \n')
		fichier.write('					<Label>System</Label>  \n')
		fichier.write('					<Letter>S</Letter>  \n')
		fichier.write('					<Format>NTFS</Format>  \n')
		fichier.write('					<Active>true</Active>  \n')
		fichier.write('				  </ModifyPartition> \n')
		fichier.write('				  <!-- Windows partition --> \n')
		fichier.write('				  <ModifyPartition wcm:action="add"> \n')
		fichier.write('					<Order>2</Order>  \n')
		fichier.write('					<PartitionID>2</PartitionID>  \n')
		fichier.write('					<Label>Windows</Label>  \n')
		fichier.write('					<Letter>C</Letter>  \n')
		fichier.write('					<Format>NTFS</Format>  \n')
		fichier.write('				  </ModifyPartition> \n')
		fichier.write('				</ModifyPartitions> \n')
		fichier.write('			  </Disk> \n')
		fichier.write('			  <WillShowUI>OnError</WillShowUI>  \n')
		fichier.write('			</DiskConfiguration> \n')
		fichier.write('			<ImageInstall> \n')
		fichier.write('                <OSImage> \n')
		fichier.write('                    <InstallFrom> \n')
		fichier.write('                        <MetaData wcm:action="add"> \n')
		fichier.write('                            <Key>/IMAGE/NAME</Key> \n')
		fichier.write('                            <Value>Windows Server 2016 SERVERSTANDARD</Value> \n')
		fichier.write('                        </MetaData> \n')
		fichier.write('                    </InstallFrom>				 \n')
		fichier.write('                    <InstallTo> \n')
		fichier.write('                        <DiskID>0</DiskID> \n')
		fichier.write('                        <PartitionID>2</PartitionID> \n')
		fichier.write('                    </InstallTo> \n')
		fichier.write('                </OSImage> \n')
		fichier.write('            </ImageInstall> \n')
		fichier.write('            <UserData> \n')
		fichier.write('                <ProductKey> \n')
		fichier.write('                    <Key>{}</Key> \n'.format(productkey))
		fichier.write('                    <WillShowUI>OnError</WillShowUI> \n')
		fichier.write('                </ProductKey> \n')
		fichier.write('                <AcceptEula>true</AcceptEula> \n')
		fichier.write('            </UserData>			 \n')
		fichier.write('        </component> \n')
		fichier.write('    </settings> \n')
		fichier.write('    <cpi:offlineImage cpi:source="wim:c:/iso/install.wim#Windows Server 2016 SERVERSTANDARD" xmlns:cpi="urn:schemas-microsoft-com:cpi" /> \n')
		fichier.write('</unattend> \n')
