let model = null;
let video = null;
let isCameraOn = false;
let detectionInterval = null;

// Existing functions
function makeMove(move) {
    fetch('/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ move: move })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `AI chose: ${data.ai_move}\n${data.result}`;
    });
}

function showStatistics() {
    fetch('/statistics')
    .then(response => response.json())
    .then(data => {
        alert(`Total games: ${data.total_games}\nUser wins: ${data.user_wins}\nAI wins: ${data.ai_wins}\nDraws: ${data.draws}`);
    });
}

function exitGame() {
    fetch('/exit')
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.close();
    });
}

// New functions for camera and hand sign recognition

async function setupCamera() {
    video = document.getElementById('video');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('getUserMedia is not supported in your browser');
        return false;
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        return new Promise((resolve) => {
            video.onloadedmetadata = () => {
                resolve(true);
            };
        });
    } catch (err) {
        alert('Error accessing camera: ' + err.message);
        return false;
    }
}

function stopCamera() {
    if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
        video.srcObject = null;
    }
    isCameraOn = false;
    clearInterval(detectionInterval);
    detectionInterval = null;
    document.getElementById('cameraStatus').innerText = 'Camera stopped.';
    document.getElementById('startCameraBtn').classList.remove('hidden');
    document.getElementById('stopCameraBtn').classList.add('hidden');
}

function classifyHandPose(landmarks) {
    // Simple heuristic to classify rock, paper, scissors based on finger curl
    // landmarks is an array of 21 points with x,y,z coordinates

    // Calculate distances between finger tips and bases to determine finger extension

    function distance(a, b) {
        return Math.sqrt(
            (a[0] - b[0]) ** 2 +
            (a[1] - b[1]) ** 2 +
            (a[2] - b[2]) ** 2
        );
    }

     // Use the wrist to scale distances (more adaptive)
     const wrist = landmarks[0];
     const scale = distance(landmarks[0], landmarks[9]); // wrist to middle base
 
     function isExtended(tip, base) {
         return distance(landmarks[tip], landmarks[base]) > 0.7 * scale;
     }
 
     const indexExtended = isExtended(8, 5);
     const middleExtended = isExtended(12, 9);
     const ringExtended = isExtended(16, 13);
     const pinkyExtended = isExtended(20, 17);
     const thumbExtended = isExtended(4, 2);
 
     // Rock: all fingers curled
     if (!indexExtended && !middleExtended && !ringExtended && !pinkyExtended && !thumbExtended) {
         return 'rock';
     }
 
     // Paper: all fingers extended
     if (indexExtended && middleExtended && ringExtended && pinkyExtended) {
         return 'paper';
     }
 
     // Scissors: only index and middle extended
     if (indexExtended && middleExtended && !ringExtended && !pinkyExtended && !thumbExtended) {
         return 'scissors';
     }
 
     return null;
}

async function detectHands() {
    if (!model || !video) return;

    const predictions = await model.estimateHands(video, true);
    if (predictions.length > 0) {
        const landmarks = predictions[0].landmarks;
        const move = classifyHandPose(landmarks);
        if (move) {
            document.getElementById('cameraStatus').innerText = `Detected move: ${move}`;
            makeMove(move);
        } else {
            document.getElementById('cameraStatus').innerText = 'Hand detected but move unclear.';
        }
    } else {
        document.getElementById('cameraStatus').innerText = 'No hand detected.';
    }
}

async function startCameraInput() {
    if (isCameraOn) return;
    const ready = await setupCamera();
    if (!ready) return;

    document.getElementById('cameraStatus').innerText = 'Camera started. Detecting hand signs...';
    document.getElementById('startCameraBtn').classList.add('hidden');
    document.getElementById('stopCameraBtn').classList.remove('hidden');

    if (!model) {
        model = await handpose.load();
    }

    isCameraOn = true;
    video.play();

    detectionInterval = setInterval(detectHands, 1000); // Detect every 1 second
}

function setupCameraButtons() {
    document.getElementById('startCameraBtn').addEventListener('click', startCameraInput);
    document.getElementById('stopCameraBtn').addEventListener('click', () => {
        stopCamera();
        document.getElementById('cameraStatus').innerText = 'Camera stopped.';
    });
}

// Initialize camera buttons on page load
window.addEventListener('load', () => {
    setupCameraButtons();
});
