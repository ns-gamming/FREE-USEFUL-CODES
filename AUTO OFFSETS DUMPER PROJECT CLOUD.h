AUTO OFFSET DUMPER BY PROJECT CLOUD
                               
IF YOU REMOVE MY NAME OR DON''T GIVE ME CREDIT "SO YOUR FULL FAMILIE MEMBER IS GAY"
                                                                
uintptr_t HeadTF = 0x1313850;
uintptr_t HipTF = 0x1313a6c;
uintptr_t ToeTF = 0x1314140;
                                                                                               
uintptr_t MainCameraTransform = 0x17c;
uintptr_t Dictionary = 0x58;
uintptr_t IsClientBot = 0x210;
uintptr_t Transform_INTERNAL_SetPosition = 0x6bc20c4;
uintptr_t Transform_INTERNAL_GetPosition = 0x6bc2024;
uintptr_t Component_GetTransform = 0x6a671bc;
uintptr_t GetPosition = 0x6bc1fdc;
uintptr_t WorldToScreenPoint = 0x6a63e88;
uintptr_t GetForward = 0x6bc2b84;
uintptr_t GetLocalPlayer = 0x21a89a4;
uintptr_t Curent_Match = 0x1ba166c;
uintptr_t Camera_main = 0x6a647fc;
uintptr_t get_IsFiring = 0x127d42c;
uintptr_t get_IsSighting = 0x127d4e4;
uintptr_t get_isLocalTeam = 0x12a77b4;
uintptr_t get_isVisible = 0x128e140;
uintptr_t get_IsDieing = 0x127cddc;
uintptr_t set_aim = 0x12867f4;
uintptr_t get_MaxHP = 0x12f8604;
uintptr_t get_CurHp = 0x12f84a8;
                                                                                               
uintptr_t Transform_GetPosition = 0x6bc2024;
uintptr_t Transform_SetPosition = 0x6bc20c4;
                                                                                               
uintptr_t Player_GetHeadCollider = 0x1288040;
uintptr_t Physics_Raycast = 0x23bb8c4;
uintptr_t U3DStr = 0x67e1f18;
uintptr_t IsCatapultFalling = 0x129fa4c;
uintptr_t OnStopCatapultFalling = 0x134c884;
uintptr_t get_MyPhsXData = 0x128d2e8;
                                                                                               
uintptr_t WeaponOnHand = 0x1284848;
uintptr_t TakeDamage = 0x12f5990;
uintptr_t StartWholeBodyFiring = 0x1943478;
uintptr_t Get_LocalPlayerOrObServer = 0x1ba256c;
                                                                                               
                                                                                               
---------------------Main.cpp Hook Offsets-------------------
                                                                                               
HOOK_LIB("libil2cpp.so", "0x12e45dc", Proxy_UpdateEsp, Orig_UpdateEsp);
HOOK_LIB("libil2cpp.so", "0x29245ac", _GetSpecialRunSpeedScale, GetSpecialRunSpeedScale);
HOOK_LIB("libil2cpp.so", "0x4d772d4", hook_ResetGuest, orig_ResetGuest);
HOOK_LIB("libil2cpp.so", "0x1278434", hook_AimSilent, orig_AimSilent);
                                                                                               
HOOK_LIB("libil2cpp.so", "0x12d3e3c", Fly_Update_old, Fly_Updatex);
HOOK_LIB("libil2cpp.so", "0x13a58c8", _IsMove, IsMove);
HOOK_LIB("libil2cpp.so", "0x12aa884", _GetPhysXPose, GetPhysXPose);
HOOK_LIB("libil2cpp.so", "0x134c884", _OnStopCatapultFalling, OnStopCatapultFalling);
                                                                                               
HOOK_LIB("libil2cpp.so", "0x1fcf320", DamageInfoHook, DamageInfo);
                                                                                               
MemoryPatch::createWithHex("libil2cpp.so", 0x4ff1900 + 116, "00 F0 20 E3", 4).Modify();
MemoryPatch::createWithHex("libil2cpp.so", 0x4b7d1a8 + 136, "00 F0 20 E3", 4).Modify();
                                                                                               
                                                                                               
---------------------Script Functions Offsets-------------------
                                                                                               
ZG_BYPASS + 116 = 0x4ff1900
ZG_BYPASS + 136 = 0x4b7d1a8
Gold Body = 0x134d440
Auto Eliminate Player = 0x5d8be24
Special Speed Player = 0x29245ac
High Camera View = 0x129fb2c
No Parachute = 0x12aa804
Fast Medkit = 0x292775c
Fast Gun Switch = 0x1289bd0
Vbadge = 0x56eb83c
CameraView = 0x1d20910
Reset Guest = 0x4d772d4
                                                                                               
                                                                                               
---------------------Extra Other Offsets-------------------
                                                                                               
uintptr_t HeadTF 2 = 0x36c;
uintptr_t HipTF 2 = 0x370;
uintptr_t ToeTF 2 = 0x384;
uintptr_t RightHandTF = 0x398;
uintptr_t LeftHandTF = 0x368;
uintptr_t EyeTF = 0x374;
uintptr_t LeftForeArmTF = 0x380;
uintptr_t RightForeArmTF = 0x3a4;
uintptr_t GetLeftAnkleTF = 0x394;
uintptr_t GetRightAnkleTF = 0x390;
uintptr_t GetLeftToeTF = 0x1314294;
uintptr_t GetRightToeTF = 0x388;
                                                                                               
uintptr_t get_MyFollowCamera = 0x128798c;
uintptr_t get_NickName = 0x1284ff0;
uintptr_t get_Chars = 0x67d17a0;
uintptr_t GetActiveWeapon = 0x1266c10;
uintptr_t GetPhysXState = 0x12aa804;
uintptr_t CurrentUIScene = 0x1b9ed90;
uintptr_t CurrentLocalPlayer = 0x1ba1c6c;
uintptr_t GetAttackableCenterWS = 0x1283f80;
uintptr_t get_InSwapWeaponCD = 0x1289bd0;
uintptr_t get_HeadShotDamageDecreaseScale = 0x292a1fc;
uintptr_t get_Itransform = 0x59911b8;
                                                                                               
uintptr_t IsCrouching = 0x12aa8fc;
uintptr_t IsFreeMove = 0x12ef448;
uintptr_t IsInstanceOf = 0x6a50814;
uintptr_t IsOnlineGame = 0x1cad834;
uintptr_t SetAimRotation = 0x1289d3c;
                                                                                               
uintptr_t Update = 0x3daec7c;
uintptr_t ShowAssistantText = 0x1479ba8;
uintptr_t ShowDynamicPopupMessage = 0x143fe00;
uintptr_t m_ShowGrenadeLine = 0x14;
uintptr_t m_GrenadeLine = 0x18;
uintptr_t DrawLine2 = 0x3db0200;
uintptr_t set_ShowGrenadeLine = 0x3dade6c;
uintptr_t set_startColor = 0x64eb3b4;
uintptr_t set_endColor = 0x64eb3d8;
uintptr_t set_PositionCount = 0x64eb400;
uintptr_t SetPosition = 0x64ebf34;
uintptr_t UpdateBehavior = 0x3a55778;
                                                                                               
CCNEAFOPMIH = 0x4b7d2f8
ADBBMDMEFNO = 0x16b0154
CPBCGAKODII = 0x526b0000 // It will not work
CPBCGAKODII2 = 0x36a2be0
LGINFBPMLAI = 0x11c150c
HBPBMIOJGFA = 0x4b4572c


// Auto Offsets Dumped By @seafreefire