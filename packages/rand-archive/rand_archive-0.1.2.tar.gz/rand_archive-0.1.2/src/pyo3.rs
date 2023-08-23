use crate::archive::{ArchiveWriter, EntryMetadata, Header};
use color_eyre::eyre::Result;
use indexmap::IndexMap;
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyDict, PyType};

impl IntoPyDict for EntryMetadata {
    fn into_py_dict(self, py: Python<'_>) -> &PyDict {
        let dict = PyDict::new(py);
        dict.set_item("start", self.start).unwrap();
        dict.set_item("end", self.end).unwrap();
        dict
    }
}

#[pyclass(name = "Header")]
#[derive(Clone, Debug)]
pub struct PyHeader {
    pub inner: Header,
}

#[pymethods]
impl PyHeader {
    #[classmethod]
    pub fn read(cls: &PyType, path: &str) -> Result<Self> {
        let inner = Header::read(path)?;
        Ok(PyHeader { inner })
    }

    pub fn inner<'a>(&self, py: Python<'a>) -> IndexMap<String, &'a PyDict> {
        let mut im = IndexMap::new();
        for (key, value) in self.inner.entries.iter() {
            im.insert(key.clone(), value.clone().into_py_dict(py));
        }
        im
    }
}

#[pyclass(name = "ArchiveWriter")]
#[derive(Clone, Debug)]
pub struct PyArchiveWriter {
    inner: ArchiveWriter,
}

#[pymethods]
impl PyArchiveWriter {
    #[new]
    #[pyo3(signature = (path, cache_size=524288000))]
    pub fn new(path: String, cache_size: usize) -> Self {
        Self {
            inner: ArchiveWriter::new(path, cache_size),
        }
    }

    #[classmethod]
    #[pyo3(signature = (path, cache_size=524288000))]
    pub fn read(cls: &PyType, path: &str, cache_size: usize) -> Result<Self> {
        let inner = ArchiveWriter::read(path, cache_size)?;
        Ok(PyArchiveWriter { inner })
    }

    pub fn write(&mut self, key: &str, value: &[u8]) -> PyResult<()> {
        self.inner.write(key, value).map_err(|e| e.into())
    }

    pub fn close(&mut self) -> PyResult<()> {
        self.inner.close().map_err(|e| e.into())
    }
}

#[pymodule]
fn rand_archive(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyHeader>()?;
    m.add_class::<PyArchiveWriter>()?;
    Ok(())
}
