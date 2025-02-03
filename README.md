## How to neue NixOS Configuration uploaden

einfach per USB anstöpseln (**vorher Stromversorgung abstecken!!!**) (das ist per CDC Ether, d.h. Windows geht da nicht, außerdem ist für Nix sowieso Linux sinnvoller)

```bash
NIXOS_BUILD_PATH=$(nix build .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --print-out-paths)
nix copy .#nixosConfigurations.tnf-abfahrtstafel.config.system.build.toplevel --to ssh://root@fe80::64a9:a1ff:fe0f:7f46%usb0
ssh root@fe80::64a9:a1ff:fe0f:7f46%usb0 $NIXOS_BUILD_PATH/bin/switch-to-configuration switch
```

## How to physisch (ab)montieren

Das Display ist mit einem 3D-Druck Gehäuse an der Wand montiert, die folgenden Schritte von oben nach unten zum Montieren und von unten nach oben zum Abmontieren befolgen:

* 3D-Druck Gehäuse mit 4 Schrauben an Wand anschrauben
* Display in 3D-Druck Gehäuse geben
* Die 4 Befestigungswinkel mit je 4 Schrauben befestigen

für die Schrauben der Befestigungswinkel sind Thread-Insets im Gehäuse verbaut

## Verbaute Hardware

* [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
* [Waveshare 13.3" e-paper mit display HAT (K)](https://www.waveshare.com/13.3inch-e-paper-hat-k.htm)

