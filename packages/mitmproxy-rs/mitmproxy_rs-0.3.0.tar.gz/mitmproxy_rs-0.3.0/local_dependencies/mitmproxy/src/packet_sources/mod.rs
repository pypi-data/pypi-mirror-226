use anyhow::Result;
use async_trait::async_trait;
use tokio::sync::{broadcast, mpsc};

use crate::messages::{NetworkCommand, NetworkEvent};

#[cfg(target_os = "macos")]
pub mod macos;
#[cfg(windows)]
pub mod windows;
pub mod wireguard;

pub mod ipc {
    include!(concat!(env!("OUT_DIR"), "/mitmproxy.ipc.rs"));
}

#[async_trait]
pub trait PacketSourceConf {
    type Task: PacketSourceTask + Send + 'static;
    type Data: Send + 'static;

    fn name(&self) -> &'static str;

    async fn build(
        self,
        net_tx: mpsc::Sender<NetworkEvent>,
        net_rx: mpsc::Receiver<NetworkCommand>,
        sd_watcher: broadcast::Receiver<()>,
    ) -> Result<(Self::Task, Self::Data)>;
}

#[async_trait]
pub trait PacketSourceTask {
    async fn run(mut self) -> Result<()>;
}
