use std::process::Command;

fn main() {
    println!("cargo:rerun-if-changed=src/oewse_pouw_kernel.cu");
    println!("cargo:rerun-if-changed=proto/pouw_mesh.proto");

    let out_dir = std::env::var("OUT_DIR").unwrap();
    let object_file = format!("{}/oewse_pouw_kernel.o", out_dir);
    let lib_file = format!("{}/liboewse_pouw.a", out_dir);

    // Compile CUDA code
    let status = Command::new("nvcc")
        .args(&[
            "-O3",
            "-c",
            "src/oewse_pouw_kernel.cu",
            "-o",
            &object_file,
            "-arch=sm_52",
            "-Xcompiler",
            "-fPIC",
        ])
        .status();

    match status {
        Ok(s) if s.success() => {
            // Archive into a static library
            let status = Command::new("ar")
                .args(&["rcs", &lib_file, &object_file])
                .status()
                .unwrap();

            if status.success() {
                println!("cargo:rustc-link-search=native={}", out_dir);
                println!("cargo:rustc-link-lib=static=oewse_pouw");
                println!("cargo:rustc-link-lib=dylib=cudart");
            }
        }
        _ => {
            println!("cargo:warning=nvcc compilation failed or not available, skipping CUDA build.");
        }
    }

    // Compile protobuf definitions
    tonic_build::configure()
        .compile(&["proto/pouw_mesh.proto"], &["proto"])
        .unwrap();
}
