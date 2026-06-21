; Inno Setup — run via desktop\build.ps1 after PyInstaller builds dist\KegelHealth.exe
; Requires Inno Setup 6: https://jrsoftware.org/isinfo.php

#define MyAppName "Kegel Health"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kegel Health"
#define MyAppExeName "KegelHealth.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\dist\installer
OutputBaseFilename=KegelHealth-Setup
SetupIconFile=assets\kegel.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\dist\KegelHealth.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "https://ollama.com/download"; Description: "Open Ollama download page (recommended for AI plans)"; Flags: postinstall shellexec unchecked
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent unchecked

[Messages]
WelcomeLabel2=This will install [name/ver] on your computer.%n%nFor personalized exercise plans, install Ollama after setup and pull a model (for example llama3.2). The app detects local models automatically.

[Code]
var
  OllamaPage: TWizardPage;
  OllamaInfo: TNewStaticText;

procedure InitializeWizard;
begin
  OllamaPage := CreateCustomPage(
    wpWelcome,
    'Local AI (Ollama)',
    'Optional but recommended for personalized plans'
  );

  OllamaInfo := TNewStaticText.Create(OllamaPage);
  OllamaInfo.Parent := OllamaPage.Surface;
  OllamaInfo.AutoSize := False;
  OllamaInfo.WordWrap := True;
  OllamaInfo.Left := ScaleX(0);
  OllamaInfo.Top := ScaleY(0);
  OllamaInfo.Width := OllamaPage.SurfaceWidth;
  OllamaInfo.Height := ScaleY(160);
  OllamaInfo.Caption :=
    'Kegel Health can generate customized plans using a local LLM via Ollama.' + #13#10 + #13#10 +
    '1. After install, download Ollama from ollama.com' + #13#10 +
    '2. Open a terminal and run: ollama pull llama3.2' + #13#10 +
    '3. Keep Ollama running while using the app' + #13#10 + #13#10 +
    'If Ollama is not installed, the app still works with a built-in template plan.';
end;
