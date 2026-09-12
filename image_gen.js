#!/usr/bin/env node

/**
 * Image Generation Skill for pi framework
 * Supports FLUX or Stable Diffusion models on CPU/GPU
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

module.exports = async function generateImage() {
  console.log("=".repeat(70));
  console.log("🖼️  Image Generation Skill");
  console.log("=".repeat(70));
  
  // Get configuration from environment or defaults
  const model = process.env.MODEL || "stable-diffusion-v1-5";
  const prompt = process.env.PROMPT || "pixel art cat";
  const numSteps = parseInt(process.env.STEPS) || 30;
  const width = parseInt(process.env.WIDTH) || 512;
  
  // Check Python availability and run generation script
  const scriptPath = path.join(__dirname, '..');
  
  try {
    return await new Promise((resolve, reject) => {
      const pythonScript = fs.existsSync(path.join(scriptPath, 'generate_cat.py')) || 
                           fs.existsSync(path.join(scriptPath, 'generate_cat_final.py')) ?
        `${scriptPath}/generate_cat.py ${prompt} -s${numSteps} -w${width}` :
        '';
      
      if (!pythonScript) {
        console.log("\nNo Python generation script found.");
        resolve({ success: false, error: "No generation script available" });
        return;
      }
      
      console.log(`\n📥 Model: ${model}`);
      console.log(`🎨 Prompt: ${prompt}`);
      console.log(`📐 Size: ${width}x${width}`);
      console.log(`⚙️  Steps: ${numSteps}\n`);
      
      const python = spawn('python', [scriptPath]);
      
      let output = '';
      
      python.stdout.on('data', data => {
        output += data.toString();
        console.log(data.toString());
      });
      
      python.stderr.on('data', data => {
        const err = data.toString();
        if (!err.includes('[Errno 2]')) {
          console.error(err);
        }
      });
      
      python.on('close', code => {
        resolve({
          success: code === 0,
          output
        });
      });
      
      python.on('error', err => {
        reject(new Error(`Python process error: ${err.message}`));
      });
    });
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Self-execution for testing
if (require.main === module) {
  generateImage()
    .then(result => {
      console.log("=".repeat(70));
      console.log(result.output || result.error);
      process.exit(result.success ? 0 : 1);
    })
    .catch(err => {
      console.error(err.message);
      process.exit(1);
    });
}
