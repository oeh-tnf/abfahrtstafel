{ config, pkgs, lib, ... }:

{

  boot.kernelModules = [
    "libcomposite"
  ];

  systemd.services.usb_otg = {
    enable = true;
    wantedBy = [ "multi-user.target" ];
    serviceConfig = {
      Type = "oneshot";
    };
    script = ''
      CONFIGFS_HOME=/sys/kernel/config
      mkdir -p $CONFIGFS_HOME/usb_gadget/g1
      cd $CONFIGFS_HOME/usb_gadget/g1

      echo 0x1d6b > idVendor
      echo 0x0104 > idProduct
      echo 0x0100 > bcdDevice
      echo 0x0200 > bcdUSB

      mkdir -p strings/0x409
      cat /sys/firmware/devicetree/base/serial-number > strings/0x409/serialnumber
      echo "OEH TNF" > strings/0x409/manufacturer
      echo "TNF Abfahrtstafel" > strings/0x409/product

      mkdir -p configs/c.1/strings/0x409
      echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
      echo 250 > configs/c.1/MaxPower

      mkdir -p functions/ecm.usb0
      echo "62:A9:A1:0F:7F:46" > functions/ecm.usb0/host_addr
      echo "66:A9:A1:0F:7F:46" > functions/ecm.usb0/dev_addr
      ln -s functions/ecm.usb0 configs/c.1/

      ls /sys/class/udc > UDC

      ${pkgs.iproute2}/bin/ip link set dev usb0 up
    '';
  };

}
