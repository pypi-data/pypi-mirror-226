use std::sync::Once;

pub mod archive;
pub mod header;
mod pyo3;

static INIT: Once = Once::new();

pub(crate) fn setup() {
    INIT.call_once(|| {
        color_eyre::install().unwrap();
    });
}
