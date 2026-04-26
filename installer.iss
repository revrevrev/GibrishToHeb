#pragma codepage 65001

[Setup]
AppName=Gibrish to Hebrew Transformer
AppVersion=1.0
AppPublisher=Revital Ferster
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
FinishedLabel=ההתקנה הושלמה בהצלחה!%n%nהוראות שימוש:%n%n  1. בחר טקסט בכל יישום%n  2. לחץ על מקש הקיצור לפתיחת חלון ההמרה%n  3. לחץ "בצע" לביצוע ההמרה, או "בטל" לביטול%n  4. הטקסט יוחלף אוטומטית באותיות עבריות%n%nהתוכנית פועלת ברקע כאייקון במגש המערכת.%nלחיצה ימנית על האייקון מאפשרת שינוי מקש הקיצור או יציאה מהתוכנית.%n%nמקש הקיצור שנבחר: {code:GetHotkeyValue}

[Code]

var
  HotkeyPage: TWizardPage;
  HotkeyCombo: TComboBox;

{ Map combo index → keyboard-library hotkey string (must match Python side) }
function GetHotkeyValue(Param: String): String;
begin
  case HotkeyCombo.ItemIndex of
    0: Result := 'f8';
    1: Result := 'f9';
    2: Result := 'f10';
    3: Result := 'f12';
    4: Result := 'ctrl+f8';
    5: Result := 'ctrl+f9';
    6: Result := 'ctrl+f10';
    7: Result := 'alt+f8';
    8: Result := 'alt+f9';
    9: Result := 'alt+f10';
  else
    Result := 'f8';
  end;
end;

procedure InitializeWizard();
var
  LabelInstr: TLabel;
begin
  HotkeyPage := CreateCustomPage(
    wpSelectDir,
    'Choose Activation Hotkey',
    'Select the key combination that will activate the Hebrew transformer.'
  );

  LabelInstr := TLabel.Create(WizardForm);
  LabelInstr.Parent := HotkeyPage.Surface;
  LabelInstr.Left := 0;
  LabelInstr.Top := 0;
  LabelInstr.Width := HotkeyPage.SurfaceWidth;
  LabelInstr.Caption := 'Press this hotkey after selecting text to open the transform dialog:';
  LabelInstr.AutoSize := True;

  HotkeyCombo := TComboBox.Create(WizardForm);
  HotkeyCombo.Parent := HotkeyPage.Surface;
  HotkeyCombo.Left := 0;
  HotkeyCombo.Top := LabelInstr.Top + LabelInstr.Height + 10;
  HotkeyCombo.Width := 180;
  HotkeyCombo.Style := csDropDownList;

  HotkeyCombo.Items.Add('F8  (default)');
  HotkeyCombo.Items.Add('F9');
  HotkeyCombo.Items.Add('F10');
  HotkeyCombo.Items.Add('F12');
  HotkeyCombo.Items.Add('Ctrl+F8');
  HotkeyCombo.Items.Add('Ctrl+F9');
  HotkeyCombo.Items.Add('Ctrl+F10');
  HotkeyCombo.Items.Add('Alt+F8');
  HotkeyCombo.Items.Add('Alt+F9');
  HotkeyCombo.Items.Add('Alt+F10');

  HotkeyCombo.ItemIndex := 0;
end;

{ Write config.json with the chosen hotkey after files are installed }
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir, ConfigFile, ConfigContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigDir     := ExpandConstant('{userappdata}\GibrishToHeb');
    ConfigFile    := ConfigDir + '\config.json';
    ConfigContent := '{"hotkey": "' + GetHotkeyValue('') + '"}';

    ForceDirectories(ConfigDir);
    SaveStringToFile(ConfigFile, ConfigContent, False);
  end;
end;
