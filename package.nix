{ lib
, python3Packages
, hatch
}:

python3Packages.buildPythonApplication rec {
  pname = "tnf_abfahrtstafel";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  nativeBuildInputs = [
    hatch
  ];

  propagatedBuildInputs = with python3Packages; [
    pillow
    requests
  ];
}
