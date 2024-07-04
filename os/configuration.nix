{ config, pkgs, lib, ... }:

{
  boot = {
    # This was necessary for testing at /dev/lol, because of 2.4/5Ghz hybrid wifi
    extraModprobeConfig = ''
      options brcmfmac roamoff=1 feature_disable=0x82000
    '';
  };

  # We need that for wifi
  hardware.enableRedistributableFirmware = true;

  age.secrets.wifi.file = secrets/wifi.age;

  networking = {
    hostName = "tnf-abfahrtstafel";
    interfaces = {
      wlan0 = {
        useDHCP = true;
      };
    };
    wireless = {
      enable = true;
      environmentFile = config.age.secrets.wifi.path;
      networks = {
        # for testing
        "/dev/lol" = {
          psk = "@PSK_DEVLOL@";
        };
      };
    };
  };

  environment.systemPackages = with pkgs; [
    vim
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

  # DO NOT CHANGE, unless you know exactly what you are doing
  system.stateVersion = "24.05";
}