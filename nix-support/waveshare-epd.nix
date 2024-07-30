{ lib
, fetchFromGitHub
, python3Packages
, rpi-gpio2
, gpiozero
, hatch
}:

python3Packages.buildPythonPackage rec {
  pname = "waveshare-epd";
  version = "0.0.1";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "waveshareteam";
    repo = "e-Paper";
    rev = "bc23f8ee814486edb6a364c802847224e079e523";
    sha256 = "sha256-Ky7Q1pRr6mXdNutOECwFHPc4CSkE6ScGzoobNAhD1gI=";
  } + "/RaspberryPi_JetsonNano/python";

  patches = [
    ./waveshare-epd.patch
  ];

  nativeBuildInputs = [
    hatch
  ];

  propagatedBuildInputs = with python3Packages; [
    pillow
    spidev
    gpiozero
    rpi-gpio2
  ];
}
