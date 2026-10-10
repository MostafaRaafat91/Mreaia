# Contributing to Mreaia (مرآيا)

Thank you for your interest in contributing to **Mreaia**! 
Mreaia is an independent research and engineering project conceived and directed by **Mostafa Raafat**, engineered with Google DeepMind Antigravity AI technology.

---

## 🤝 Code of Conduct & Commercial Licensing Notice
- **Non-Commercial Research & Community Use:** Mreaia source code is public and source-available for personal, educational, and academic research purposes.
- **Commercial Rights:** All commercial monetization, proprietary SaaS hosting, and closed redistribution rights are **strictly reserved to Mostafa Raafat**.
- For commercial licensing or enterprise inquiries, contact the author via [GitHub](https://github.com/MostafaRaafat91).

---

## 🛠️ How to Contribute

We welcome community contributions in the following areas:

1. **New File Format Distillers:**
   - Adding extractors for 3D model files (`.obj`, `.gltf`, `.stl`).
   - Adding extractors for geospatial formats (`.geojson`, `.kml`, `.shp`).
   - Adding specialized CAD or scientific datasets (`.h5`, `.parquet`, `.fits`).

2. **Benchmark Reporting:**
   - Submitting empirical compression ratios and token saving benchmarks across different file types and LLMs.

3. **Bug Reports & Security Audits:**
   - Reporting cryptographic edge cases, hardware UUID edge cases on Linux distros or Windows, or performance bottlenecks.

---

## 🚀 Development Setup

```bash
# 1. Fork & clone the repository
git clone https://github.com/MostafaRaafat91/Mreaia.git
cd Mreaia

# 2. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run the automated test suite
python test_mreaia.py
```

All pull requests must pass the `test_mreaia.py` automated test suite before review.

Thank you for supporting **Mreaia**! ⭐
