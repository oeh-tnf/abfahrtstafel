{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-24.05;
    systems.url = github:nix-systems/default;
    nixos-hardware.url = github:NixOS/nixos-hardware/master;

    agenix.url = github:ryantm/agenix;
    agenix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, systems, agenix, nixos-hardware }: {
    packages =
      let
        eachSystem = nixpkgs.lib.genAttrs (import systems);
      in
      eachSystem (system: {
        hatch = nixpkgs.legacyPackages.${system}.hatch.overridePythonAttrs (old: {
          # need to disable some tests for successful build on aarch64-linux
          disabledTests = old.disabledTests ++ [
            "test_field_readme"
            "test_field_string"
            "test_field_complex"
            "test_plugin_dependencies_unmet"
          ];
        });
        default = nixpkgs.legacyPackages.${system}.callPackage app/package.nix {
          waveshare-epd = self.packages.${system}.waveshare-epd;
          hatch = self.packages.${system}.hatch;
        };
        waveshare-epd = nixpkgs.legacyPackages.${system}.callPackage nix-support/waveshare-epd.nix {
          hatch = self.packages.${system}.hatch;
        };
      });
    apps =
      let
        eachSystem = nixpkgs.lib.genAttrs (import systems);
      in
      eachSystem (system: {
        agenix = {
          type = "app";
          program = "${agenix.packages.${system}.agenix}/bin/agenix";
        };
      });
    nixosConfigurations.tnf-abfahrtstafel = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      specialArgs = {
        abfahrtstafel-pkg = self.packages.aarch64-linux.default;
      };
      modules = [
        "${nixpkgs}/nixos/modules/installer/sd-card/sd-image-aarch64.nix"
        "${nixos-hardware}/raspberry-pi/4/pkgs-overlays.nix"
        agenix.nixosModules.default
        os/configuration.nix
      ];
    };
  };
}

