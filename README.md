## How to neue NixOS Configuration uploaden

einfach per USB anstöpseln (das ist per CDC Ether, d.h. Windows geht da nicht, außerdem ist für Nix sowieso Linux sinnvoller)

```bash
NIXOS_BUILD_PATH=$(nix build .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --print-out-paths)
nix copy .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --to ssh://root@fe80::64a9:a1ff:fe0f:7f46%usb0
ssh root@fe80::64a9:a1ff:fe0f:7f46%usb0 $NIXOS_BUILD_PATH/bin/switch-to-configuration switch
```

oder wenn man ÖH Büro WLAN ist:

```bash
NIXOS_BUILD_PATH=$(nix build .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --print-out-paths)
nix copy .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --to ssh://root@tnf-abfahrtstafel.lan
ssh root@tnf-abfahrtstafel.lan $NIXOS_BUILD_PATH/bin/switch-to-configuration switch
```
