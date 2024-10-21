{ config, pkgs, lib, ... }:

{

  # this exists in there, we just use that one part
  hardware.raspberry-pi."4".apply-overlays-dtmerge.enable = true;

  hardware.deviceTree.overlays = [
    {
      name = "spi0-1cs";
      # copied from https://github.com/raspberrypi/linux/blob/475cddaba6b02584157e1c128a5a6858770a3d06/arch/arm/boot/dts/overlays/spi0-1cs-overlay.dts
      # changed bcm2835 to bcm2837
      dtsText = ''
        /dts-v1/;
        /plugin/;


        / {
            compatible = "brcm,bcm2837";

            fragment@0 {
                target = <&spi>;
                frag0: __overlay__ {
                    pinctrl-names = "default";
                    pinctrl-0 = <&spi0_gpio7>;
                    cs-gpios = <&gpio 8 1>;

                    status = "okay";

                    spidev0: spidev@0 {
                        compatible = "spidev";
                        reg = <0>;  /* CE0 */
                        #address-cells = <1>;
                        #size-cells = <0>;
                        spi-max-frequency = <125000000>;
                    };
                };
            };

            fragment@1 {
                target = <&gpio>;
                frag1: __overlay__ {
                    pinctrl-0 = <&gpioout>;
                };
            };
        /*
            fragment@0 {
                target = <&spi0_cs_pins>;
                frag0: __overlay__ {
                    brcm,pins = <8>;
                };
            };

            fragment@1 {
                target = <&spi0>;
                frag1: __overlay__ {
                    cs-gpios = <&gpio 8 1>;
                    status = "okay";
                };
            };

            fragment@2 {
                target = <&spidev1>;
                __overlay__ {
                    status = "disabled";
                };
            };

            fragment@3 {
                target = <&spi0_pins>;
                __dormant__ {
                    brcm,pins = <10 11>;
                };
            };

            __overrides__ {
                cs0_pin  = <&frag0>,"brcm,pins:0",
                    <&frag1>,"cs-gpios:4";
                no_miso = <0>,"=3";
            };
        */
        };
      '';
    }
  ];

  systemd.services.spidev-bind = {
    enable = true;
    wantedBy = [ "multi-user.target" ];
    serviceConfig = {
      Type = "oneshot";
    };
    script = ''
      sleep 10s
      echo spidev >/sys/bus/spi/devices/spi0.0/driver_override
      echo spi0.0 >/sys/bus/spi/drivers/spidev/bind
    '';
  };
}
