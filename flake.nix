{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-24.05;
    systems.url = github:nix-systems/default;

    agenix.url = github:ryantm/agenix;
    agenix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, systems, agenix }: {
    packages =
      let
        eachSystem = nixpkgs.lib.genAttrs (import systems);
      in
      eachSystem (system: {
        default = nixpkgs.legacyPackages.${system}.callPackage app/package.nix {
          waveshare-epd = self.packages.${system}.waveshare-epd;
        };
        waveshare-epd = nixpkgs.legacyPackages.${system}.callPackage nix-support/waveshare-epd.nix {};
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
      modules = [
        "${nixpkgs}/nixos/modules/installer/sd-card/sd-image-aarch64.nix"
        agenix.nixosModules.default
        os/configuration.nix
      ];
    };
  };
}

