{ config, pkgs, lib, abfahrtstafel-pkg, ... }:

{
  imports = [
    ./usb_otg.nix
    ./spi.nix
  ];

  boot = {
    # This was necessary for testing at /dev/lol, because of 2.4/5Ghz hybrid wifi
    extraModprobeConfig = ''
      options brcmfmac roamoff=1 feature_disable=0x82000
    '';
  };

  hardware.deviceTree.overlays = [
    {
      name = "putThatDamnRevisionInThere";
      dtsText = ''
        /dts-v1/;
        /plugin/;

        / {
          compatible = "brcm,bcm2837";

          fragment@0 {
            target-path = "/";
            __overlay__ {
              system {
                linux,revision = <0x902120>;
              };
            };
          };
        };
      '';
    }
  ];

  # We need that for wifi
  hardware.enableRedistributableFirmware = true;

  hardware.deviceTree.filter = "bcm2837-rpi-*.dtb";

  age.secrets.wifi.file = secrets/wifi.age;

  networking = {
    hostName = "tnf-abfahrtstafel";
    useDHCP = false;
    interfaces = {
      wlan0 = {
        useDHCP = true;
      };
      usb0 = {
        useDHCP = false;
      };
    };
    wireless = {
      enable = true;
      environmentFile = config.age.secrets.wifi.path;
      networks = {
        "KEPLERnet" = {
          psk = "@PSK_KEPLERNET@";
        };
        # for testing
        "/dev/lol" = {
          psk = "@PSK_DEVLOL@";
        };
      };
    };
  };

  environment.systemPackages = with pkgs; [
    vim
    dtc
  ];

  users = {
    mutableUsers = false;
    users.root = {
      openssh.authorizedKeys.keys = builtins.concatMap (admin: admin.sshKeys) (builtins.attrValues (import ../admins));
    };
  };

  services.openssh = {
    enable = true;
    settings = {
      PasswordAuthentication = false;
    };
  };

  systemd.services.abfahrtstafel-update = {
    enable = true;
    serviceConfig = {
      Type = "oneshot";
      TimeoutStartSec = "45";
    };
    script = "${abfahrtstafel-pkg}/bin/tnf-abfahrtstafel-epaper";
    after = [ "spidev-bind.service" ];
  };

  systemd.timers.abfahrtstafel-update = {
    enable = true;
    wantedBy = [ "multi-user.target" ];
    after = [ "spidev-bind.service" ];
    timerConfig = {
      OnCalendar = "minutely";
    };
  };

  # DO NOT CHANGE, unless you know exactly what you are doing
  system.stateVersion = "24.05";
}
