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
; Suppress the built-in "close applications" dialog — we handle it in [Code]
CloseApplications=no
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
FinishedLabel=ההתקנה הושלמה בהצלחה!

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

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    WizardForm.FinishedLabel.AutoSize := True;
    WizardForm.FinishedLabel.Caption :=
      'ההתקנה הושלמה בהצלחה!' + #13#10 + #13#10 +
      'הוראות שימוש:' + #13#10 + #13#10 +
      '  1. בחר טקסט בכל יישום' + #13#10 +
      '  2. לחץ על מקש הקיצור לפתיחת חלון ההמרה' + #13#10 +
      '  3. לחץ "בצע" לביצוע ההמרה, או "בטל" לביטול' + #13#10 +
      '  4. הטקסט יוחלף אוטומטית באותיות עבריות' + #13#10 + #13#10 +
      'התוכנית פועלת ברקע כאייקון במגש המערכת.' + #13#10 +
      'לחיצה ימנית על האייקון מאפשרת שינוי מקש הקיצור או יציאה מהתוכנית.' + #13#10 + #13#10 +
      'מקש הקיצור שנבחר: ' + GetHotkeyValue('');
  end;
end;

{ Write config.json with the chosen hotkey after files are installed }
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir, ConfigFile, ConfigContent: String;
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    { Silently kill any running instance so the EXE file can be replaced.
      taskkill exits with 128 when the process isn't found — that's fine. }
    ShellExec('', ExpandConstant('{sys}\taskkill.exe'), '/F /IM GibrishToHeb.exe',
              '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Sleep(500);  { Give Windows time to release the file handle }
  end;

  if CurStep = ssPostInstall then
  begin
    ConfigDir     := ExpandConstant('{userappdata}\GibrishToHeb');
    ConfigFile    := ConfigDir + '\config.json';
    ConfigContent := '{"hotkey": "' + GetHotkeyValue('') + '"}';

    ForceDirectories(ConfigDir);
    SaveStringToFile(ConfigFile, ConfigContent, False);
  end;
end;
