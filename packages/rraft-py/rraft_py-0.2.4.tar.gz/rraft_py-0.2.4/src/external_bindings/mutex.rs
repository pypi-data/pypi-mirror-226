use pyo3::prelude::*;

use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Clone)]
#[pyclass(name = "Mutex")]
pub struct PyMutex {
    pub inner: Arc<Mutex<u64>>,
}

impl PyMutex {
    #[tokio::main]
    pub async fn acquire_lock_and<T>(&self, cb: impl FnOnce() -> PyResult<T>) -> PyResult<T> {
        let mut guard = self.inner.lock().await;

        // Wait until the guard's int value becomes 0.
        while *guard != 0 {
            tokio::task::yield_now().await;
            guard = self.inner.lock().await;
        }

        // Prevent interrupting stdout from Python
        Python::with_gil(|_py| {
            // The guard will be dropped when after cb executed.
            cb()
        })
    }
}

#[pymethods]
impl PyMutex {
    #[new]
    pub fn new() -> Self {
        Self {
            inner: Arc::new(Mutex::new(0)),
        }
    }

    pub fn incr(&self) -> PyResult<()> {
        let inner = self.inner.clone();

        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(async {
            let mut guard = inner.lock().await;
            *guard += 1;
        });

        Ok(())
    }

    pub fn decr(&self) -> PyResult<()> {
        let inner = self.inner.clone();

        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(async {
            let mut guard = inner.lock().await;
            *guard -= 1;
        });

        Ok(())
    }
}
