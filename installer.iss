#pragma codepage 65001

[Setup]
AppName=Gibrish to Hebrew Transformer
AppVersion=1.0
AppPublisher=revrevrev
DefaultDirName={localappdata}\GibrishToHeb
DefaultGroupName=GibrishToHeb
UninstallDisplayIcon={app}\GibrishToHeb.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=GibrishToHeb_Setup
; No admin rights needed - installs to user's AppData
PrivilegesRequired=lowest

[Files]
Source: "dist\GibrishToHeb.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; Add to Windows startup for the current user
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "GibrishToHeb"; \
  ValueData: """{app}\GibrishToHeb.exe"""; \
  Flags: uninsdeletevalue

[Icons]
Name: "{group}\Gibrish to Hebrew Transformer"; Filename: "{app}\GibrishToHeb.exe"
Name: "{group}\Uninstall GibrishToHeb"; Filename: "{uninstallexe}"

[Run]
; Offer to launch the program right after install
Filename: "{app}\GibrishToHeb.exe"; \
  Description: "Launch Gibrish to Hebrew Transformer now"; \
  Flags: postinstall nowait skipifsilent

[Messages]
FinishedLabel=ההתקנה הושלמה בהצלחה!%n%nהוראות שימוש:%n%n  1. בחר טקסט בכל יישום%n  2. לחץ F8 לפתיחת תפריט ההמרה%n  3. לחץ "המר לעברית" או Enter%n  4. הטקסט יוחלף אוטומטית באותיות עבריות%n%nהתוכנית תופעל אוטומטית עם הפעלת Windows.%nלסיום הפעלת התוכנית: לחץ Ctrl+C בחלון הטרמינל.
