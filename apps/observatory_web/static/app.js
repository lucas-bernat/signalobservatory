const statusElements = {
  connection: document.querySelector("#connectionState"),
  host: document.querySelector("#hostReadout"),
  source: document.querySelector("#sourceReadout"),
  sourceMode: document.querySelector("#sourceModeReadout"),
  sourceAcquisition: document.querySelector("#sourceAcquisitionReadout"),
  sourceHardware: document.querySelector("#sourceHardwareReadout"),
  sampleRate: document.querySelector("#sampleRateReadout"),
  fftSize: document.querySelector("#fftSizeReadout"),
  binSpacing: document.querySelector("#binSpacingReadout"),
  lastFrame: document.querySelector("#lastFrameReadout"),
  peaks: document.querySelector("#peakReadouts"),
  refreshButton: document.querySelector("#refreshButton"),
  pathDiagram: document.querySelector("#pathDiagram"),
};

const spectrumCanvas = document.querySelector("#spectrumCanvas");
const waveformCanvas = document.querySelector("#waveformCanvas");
const spectrumContext = spectrumCanvas.getContext("2d");
const waveformContext = waveformCanvas.getContext("2d");

const numberFormat = new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 });
const frequencyFormat = new Intl.NumberFormat("en-US", { maximumFractionDigits: 3 });

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function formatHz(value) {
  if (value >= 1_000_000) return `${numberFormat.format(value / 1_000_000)} MHz`;
  if (value >= 1_000) return `${numberFormat.format(value / 1_000)} kHz`;
  return `${numberFormat.format(value)} Hz`;
}

function formatTime(unixSeconds) {
  return new Date(unixSeconds * 1000).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

async function getJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path} returned ${response.status}`);
  return response.json();
}

async function refreshDashboard() {
  try {
    const [status, spectrum] = await Promise.all([
      getJson("/api/status"),
      getJson("/api/spectrum"),
    ]);

    renderStatus(status, spectrum);
    drawSpectrum(spectrum);
    drawWaveform(spectrum);
    setConnectionState(true);
  } catch (error) {
    setConnectionState(false);
    drawError(spectrumContext, spectrumCanvas, "Spectrum API unavailable");
    drawError(waveformContext, waveformCanvas, "Waveform API unavailable");
  }
}

function setConnectionState(isConnected) {
  statusElements.connection.textContent = isConnected ? "Live" : "Offline";
  statusElements.connection.classList.toggle("is-offline", !isConnected);
}

function renderStatus(status, spectrum) {
  const sourceMetadata = status.source_metadata || {};

  statusElements.host.textContent = status.hostname;
  statusElements.source.textContent = sourceMetadata.display_name || spectrum.source;
  statusElements.sourceMode.textContent = sourceMetadata.mode || "-";
  statusElements.sourceAcquisition.textContent = sourceMetadata.acquisition || "-";
  statusElements.sourceHardware.textContent = sourceMetadata.hardware || "-";
  statusElements.sampleRate.textContent = `${formatHz(spectrum.sample_rate_hz)}`;
  statusElements.fftSize.textContent = numberFormat.format(spectrum.fft_size);
  statusElements.binSpacing.textContent = `${frequencyFormat.format(spectrum.bin_spacing_hz)} Hz`;
  statusElements.lastFrame.textContent = formatTime(spectrum.generated_at);

  const chips = spectrum.peaks.map((peak) => {
    const chip = document.createElement("span");
    chip.className = "peak-chip";
    chip.style.setProperty("--peak-color", peak.color);
    chip.textContent = `${formatHz(peak.bin_frequency_hz)} at ${peak.db.toFixed(1)} dB`;
    return chip;
  });
  statusElements.peaks.replaceChildren(...chips);
  renderSignalPath(sourceMetadata.signal_path);
}

function renderSignalPath(signalPath = []) {
  const steps = signalPath.length
    ? signalPath
    : ["Source", "Samples", "FFT", "Browser Plot"];
  const nodes = steps.map((step) => {
    const node = document.createElement("span");
    node.textContent = step;
    return node;
  });

  statusElements.pathDiagram.replaceChildren(...nodes);
}

function drawFrame(context, canvas, title) {
  context.clearRect(0, 0, canvas.width, canvas.height);

  const background = context.createLinearGradient(0, 0, canvas.width, 0);
  background.addColorStop(0, "#fbfdff");
  background.addColorStop(1, "#f4f8fb");
  context.fillStyle = background;
  context.fillRect(0, 0, canvas.width, canvas.height);

  context.fillStyle = "#172033";
  context.font = "700 22px Arial, sans-serif";
  context.fillText(title, 28, 38);
}

function drawSpectrum(data) {
  const context = spectrumContext;
  const canvas = spectrumCanvas;
  drawFrame(context, canvas, "FFT magnitude spectrum");

  const bounds = {
    left: 72,
    right: canvas.width - 28,
    top: 64,
    bottom: canvas.height - 58,
  };
  const width = bounds.right - bounds.left;
  const height = bounds.bottom - bounds.top;
  const dbFloor = data.db_floor;

  function xForFrequency(frequencyHz) {
    return bounds.left + (frequencyHz / data.max_frequency_hz) * width;
  }

  function yForDb(dbValue) {
    const normalized = (clamp(dbValue, dbFloor, 0) - dbFloor) / Math.abs(dbFloor);
    return bounds.bottom - normalized * height;
  }

  context.strokeStyle = "#d8e1eb";
  context.lineWidth = 1;
  context.strokeRect(bounds.left, bounds.top, width, height);

  context.font = "700 12px Arial, sans-serif";
  context.fillStyle = "#667085";
  for (let db = 0; db >= dbFloor; db -= 15) {
    const y = yForDb(db);
    context.strokeStyle = "#e7edf4";
    context.beginPath();
    context.moveTo(bounds.left, y);
    context.lineTo(bounds.right, y);
    context.stroke();
    context.fillText(`${db} dB`, 22, y + 4);
  }

  for (let frequency = 0; frequency <= data.max_frequency_hz; frequency += 2_000) {
    const x = xForFrequency(frequency);
    context.strokeStyle = "#eef2f7";
    context.beginPath();
    context.moveTo(x, bounds.top);
    context.lineTo(x, bounds.bottom);
    context.stroke();
    context.fillText(`${frequency / 1_000} kHz`, x - 18, bounds.bottom + 28);
  }

  context.strokeStyle = "#0f766e";
  context.lineWidth = 1.6;
  context.beginPath();
  data.spectrum.forEach((point, index) => {
    const x = xForFrequency(point.frequency_hz);
    const y = yForDb(point.db);
    if (index === 0) context.moveTo(x, y);
    else context.lineTo(x, y);
  });
  context.stroke();

  data.peaks.forEach((peak) => {
    const x = xForFrequency(peak.bin_frequency_hz);
    const y = yForDb(peak.db);
    context.strokeStyle = peak.color;
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(x, bounds.top);
    context.lineTo(x, bounds.bottom);
    context.stroke();

    context.fillStyle = peak.color;
    context.beginPath();
    context.arc(x, y, 5, 0, 2 * Math.PI);
    context.fill();

    context.font = "700 14px Arial, sans-serif";
    context.fillText(formatHz(peak.bin_frequency_hz), x + 8, Math.max(bounds.top + 18, y - 10));
  });
}

function drawWaveform(data) {
  const context = waveformContext;
  const canvas = waveformCanvas;
  drawFrame(context, canvas, "Time-domain waveform");

  const bounds = {
    left: 72,
    right: canvas.width - 28,
    top: 62,
    bottom: canvas.height - 46,
  };
  const width = bounds.right - bounds.left;
  const height = bounds.bottom - bounds.top;
  const centerY = bounds.top + height / 2;
  const maxTime = data.waveform[data.waveform.length - 1]?.time_ms || 4;

  function xForTime(timeMs) {
    return bounds.left + (timeMs / maxTime) * width;
  }

  function yForAmplitude(amplitude) {
    return centerY - clamp(amplitude, -1, 1) * (height * 0.42);
  }

  context.strokeStyle = "#d8e1eb";
  context.lineWidth = 1;
  context.strokeRect(bounds.left, bounds.top, width, height);

  context.strokeStyle = "#9aa8b6";
  context.beginPath();
  context.moveTo(bounds.left, centerY);
  context.lineTo(bounds.right, centerY);
  context.stroke();

  context.font = "700 12px Arial, sans-serif";
  context.fillStyle = "#667085";
  for (let tickMs = 0; tickMs <= 4; tickMs += 1) {
    const x = xForTime(tickMs);
    context.strokeStyle = "#eef2f7";
    context.beginPath();
    context.moveTo(x, bounds.top);
    context.lineTo(x, bounds.bottom);
    context.stroke();
    context.fillText(`${tickMs} ms`, x - 12, bounds.bottom + 26);
  }

  context.strokeStyle = "#2563eb";
  context.lineWidth = 2;
  context.beginPath();
  data.waveform.forEach((point, index) => {
    const x = xForTime(point.time_ms);
    const y = yForAmplitude(point.amplitude);
    if (index === 0) context.moveTo(x, y);
    else context.lineTo(x, y);
  });
  context.stroke();
}

function drawError(context, canvas, message) {
  drawFrame(context, canvas, message);
  context.fillStyle = "#991b1b";
  context.font = "700 16px Arial, sans-serif";
  context.fillText("The local server did not return data.", 28, 74);
}

statusElements.refreshButton.addEventListener("click", refreshDashboard);
refreshDashboard();
setInterval(refreshDashboard, 1000);
