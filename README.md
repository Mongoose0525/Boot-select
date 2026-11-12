Vibe cooded boot selection screen where you can launch steam from.
You can also launch cmd or windows settings as well as having easy access to default power options from windows (shutdown, restart log off/sign out)

The interface is straight-forward and doesn't need much explaining:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7a3499d1-a757-4bdc-a4ce-a61e0836a199" />

You make your choise and then confirm it
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3cedb130-7ee9-4001-98ec-0647992bdda5" />

Supports mouse, keyboard and gamepads
<img width="990" height="540" alt="image" src="https://github.com/user-attachments/assets/f46ec4aa-9d46-4126-9ed1-41c7d58d15ab" />
<img width="990" height="540" alt="image" src="https://github.com/user-attachments/assets/abe272db-8756-47a0-b259-b08d32082613" />

Features settings and shutdown options

<img width="337" height="540" alt="2026-11-12 17-30-54-836" src="https://github.com/user-attachments/assets/56148980-988f-441a-a274-a0a6ffabb8ae" />


<img width="337" height="307" alt="image" src="https://github.com/user-attachments/assets/583c21ed-db31-4eb9-a222-2bbaf6244703" />
<img width="337" height="307" alt="image" src="https://github.com/user-attachments/assets/08316c11-b986-447c-837f-e4b251e1ea95" />
<img width="337" height="307" alt="image" src="https://github.com/user-attachments/assets/b6ffecc0-a67a-43b5-b05d-883bca33e765" />
<img width="337" height="307" alt="image" src="https://github.com/user-attachments/assets/2e260879-0cd6-46f3-bce5-7c65a61ec17d" />

shutdown prompt:
<img width="953" height="736" alt="2026-11-12 17-36-05-114" src="https://github.com/user-attachments/assets/ac5f94c3-2141-45c6-b68b-7ccf794872ea" />

Below you'll see how to setup it up:

BUT first to avoid getting stuck in Steam Big Picture, add Windows Explorer as a third-party game in Steam.

File path: C:\Windows\explorer.exe
To customize its appearance, all the decals are included in Assets\BootDecals\ExplorerDecals (SteamGridDB).
Credit: [CodingFox](https://www.steamgriddb.com/profile/76561199017990155) and [Gryelnx](https://www.steamgriddb.com/profile/76561198382055805) on [SteamGridDB](https://www.steamgriddb.com/game/5277921)

Of course, you can configure the logon shell yourself, but I made a standalone application for that.

To open the Logon Changer, either:
- Double click Logon Changer shortcut
- Run Host.exe with "-logon" or "-logonchanger" as a command-line argument.
- Go to Tools and run a standalone version of it
It doesn't matter how you type it; uppercase and lowercase both work.

Then:
1. Click "Set Boot Select (Host.exe) as Logon". 
(if you use the standalone version you'll have to select Host.exe as your logon)
2. CAREFULLY read the warning.
3. You're done!

To "uninstall" Boot Select:
1. Open the Logon Changer again.
2. Click "Restore Explorer".
3. Confirm the change.

If you get the "Steam is not detected on your device." error, open debug.cfg and set "UseSteamUrls" to true.
This makes Boot Select (Host.exe) use Steam URLs instead of searching the registry for steam.exe. (ex. steam://open/bigpicture)


As a note:

Boot Select does NOT replace or modify explorer.exe directly. Instead, it changes the registry value at:

HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Winlogon

Specifically, it changes the "Shell" string value. (no way sherlock)

The application checks whether Steam is installed by looking in these registry locations:

- HKEY_CURRENT_USER\Software\Valve\Steam
- HKEY_LOCAL_MACHINE\Software\Valve\Steam
- HKEY_LOCAL_MACHINE\Software\WOW6432Node\Valve\Steam
