import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, Optional, List
import google.generativeai as genai


class LinkedInScraper:
    def __init__(self, li_at_cookie: str):
        """
        Inisialisasi LinkedIn Scraper dengan li_at cookie
        
        Args:
            li_at_cookie: LinkedIn session cookie (li_at value)
        """
        self.li_at_cookie = li_at_cookie
        self.driver = None
        
    def _init_driver(self):
        """Inisialisasi Selenium WebDriver - Optimized untuk Docker & Ubuntu 24.04"""
        chrome_options = Options()
        
        # Headless mode (new method untuk Chrome 120+)
        chrome_options.add_argument("--headless=new")
        
        # Docker & Linux optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Window size untuk headless
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Anti-detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimizations
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-extensions")
        
        # Logging suppression
        chrome_options.add_argument("--log-level=3")
        
        # User-Agent untuk menghindari deteksi headless
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def _set_cookie(self):
        """Set li_at cookie ke browser"""
        self.driver.get("https://www.linkedin.com")
        time.sleep(2)
        
        self.driver.add_cookie({
            "name": "li_at",
            "value": self.li_at_cookie,
            "domain": ".linkedin.com"
        })
        
        time.sleep(1)
    
    def _scroll_and_wait(self, pixels: int = 500, wait_time: float = 1.5):
        """Scroll dan tunggu untuk trigger lazy loading"""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(wait_time)
    
    def _clean_text(self, text: str) -> Optional[str]:
        """Bersihkan text dari duplikasi dan whitespace"""
        if not text:
            return None
        
        lines = text.split('\n')
        cleaned_lines = []
        prev_line = None
        
        for line in lines:
            line = line.strip()
            if line and line != prev_line:
                cleaned_lines.append(line)
                prev_line = line
        
        result = '\n'.join(cleaned_lines).strip()
        return result if result else None
    
    def _get_unique_text(self, element) -> Optional[str]:
        """
        Ambil text dari element dengan handling duplikasi LinkedIn
        LinkedIn sering render text 2x untuk accessibility
        """
        try:
            # Cari span dengan aria-hidden="true" (yang visible)
            visible_span = element.find_element(By.XPATH, ".//span[@aria-hidden='true']")
            text = self._clean_text(visible_span.text)
            return text
        except:
            # Fallback ke text biasa
            return self._clean_text(element.text)
    
    def scrape_profile(self, vanity_name: str) -> Dict:
        """
        Scrape profil LinkedIn berdasarkan vanity name
        
        Args:
            vanity_name: Vanity name LinkedIn (contoh: naufal-arga-a5b22b2aa)
            
        Returns:
            Dictionary berisi data profil
        """
        try:
            print(f"\n{'='*60}")
            print(f"[SCRAPER] Starting profile scrape for: {vanity_name}")
            print(f"{'='*60}\n")
            
            self._init_driver()
            self._set_cookie()
            
            profile_url = f"https://www.linkedin.com/in/{vanity_name}/"
            print(f"[SCRAPER] Loading URL: {profile_url}")
            self.driver.get(profile_url)
            
            # Wait for profile content to load
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "profile-content"))
                )
                print("✓ Profile content loaded")
            except:
                print("⚠ Timeout waiting for profile-content, continuing anyway...")
                time.sleep(3)
            
            # Progressive scroll untuk trigger lazy loading semua section
            print("[SCRAPER] Scrolling to load all sections...")
            for i in range(5):
                self._scroll_and_wait(600, 1.0)
                print(f"[SCRAPER] Scroll iteration {i+1}/5 completed")
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            profile_data = self._extract_profile_data()
            
            print(f"\n[SCRAPER] Profile extraction completed")
            print(f"[SCRAPER] Response: {json.dumps(profile_data, indent=2, ensure_ascii=False)}\n")
            
            return profile_data
            
        except Exception as e:
            error_msg = f"Error scraping profile: {str(e)}"
            print(f"\n[SCRAPER ERROR] {error_msg}")
            import traceback
            print(f"[SCRAPER TRACEBACK]\n{traceback.format_exc()}\n")
            return {
                "data": {},
                "message": f"Error: {str(e)}"
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_profile_data(self) -> Dict:
        """Extract data dari halaman profil LinkedIn"""
        data = {
            "data": {},
            "message": "ok"
        }
        
        try:
            profile_data = {}
            
            # Full Name - dengan aria-hidden handling
            # Full Name - XPath: /html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1
            try:
                name_elem = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1")
                full_name = self._clean_text(name_elem.text)
                profile_data["full_name"] = full_name
            except:
                profile_data["full_name"] = None
            
            # Headline
            try:
                headline_elem = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]")
                profile_data["headline"] = self._clean_text(headline_elem.text)
            except:
                profile_data["headline"] = None
            
            # Location
            try:
                location_elem = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]")
                profile_data["location"] = self._clean_text(location_elem.text)
            except:
                profile_data["location"] = None
            
            # About
            try:
                about_text = None
                
                # Coba klik tombol "lihat lebih banyak" untuk section[3]
                try:
                    see_more_btn = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[3]/div[3]//button[contains(text(), 'lihat lebih banyak') or contains(text(), 'see more')]")
                    self.driver.execute_script("arguments[0].click();", see_more_btn)
                    time.sleep(1)
                except:
                    pass
                
                # Coba extract dari section[3] terlebih dahulu
                try:
                    about_elem = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[3]/div[3]/div/div/div/span[1]")
                    about_text = self._clean_text(about_elem.text)
                except:
                    pass
                
                # Jika section[3] tidak ada, coba klik tombol "lihat lebih banyak" untuk section[2]
                if not about_text:
                    try:
                        see_more_btn = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[2]/div[3]//button[contains(text(), 'lihat lebih banyak') or contains(text(), 'see more')]")
                        self.driver.execute_script("arguments[0].click();", see_more_btn)
                        time.sleep(1)
                    except:
                        pass
                    
                    # Extract dari section[2]
                    try:
                        about_elem = self.driver.find_element(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]")
                        about_text = self._clean_text(about_elem.text)
                    except:
                        pass
                
                profile_data["about"] = about_text if about_text else None
            except:
                profile_data["about"] = None
            
            # Extract sections (sudah di-scroll sebelumnya)
            profile_data["experiences"] = self._extract_experiences()
            profile_data["educations"] = self._extract_education()
            profile_data["certifications"] = self._extract_certifications()
            
            # Extract skills dengan fallback ke AI generation
            skills = self._extract_skills()
            if not skills:
                print("[SKILLS] Ekstraksi skills gagal, mencoba generate dengan AI...")
                skills = self._generate_skills_with_ai(
                    headline=profile_data.get("headline", ""),
                    about=profile_data.get("about", ""),
                    experiences=profile_data.get("experiences", [])
                )
                if skills:
                    print(f"[SKILLS] AI generation berhasil: {skills}")
                else:
                    print("[SKILLS] AI generation juga gagal")
            
            profile_data["skills"] = skills
            
            data["data"] = profile_data
            return data
            
        except Exception as e:
            print(f"Error extracting profile data: {str(e)}")
            return data
    
    def _extract_experiences(self) -> List[Dict]:
        """Extract pengalaman kerja dengan handling duplikasi LinkedIn"""
        experiences = []
        try:
            print(f"\n[EXTRACT_EXP] Starting experience extraction...")
            
            # Wait for sections to be available
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section"))
                )
                print("[EXTRACT_EXP] Sections loaded successfully")
            except Exception as wait_err:
                print(f"[EXTRACT_EXP] ⚠ Timeout waiting for sections: {str(wait_err)}")
            
            # Cari semua section untuk detect experience
            sections = self.driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section")
            print(f"[EXTRACT_EXP] Found {len(sections)} total sections")
            
            exp_section_idx = None
            
            for idx, section in enumerate(sections, start=1):
                try:
                    section_id = section.get_attribute("id")
                    if section_id and "experience" in section_id.lower():
                        exp_section_idx = idx
                        break
                except:
                    pass
            
            if not exp_section_idx:
                # Fallback: cek berdasarkan heading
                for idx, section in enumerate(sections, start=1):
                    try:
                        heading = section.find_element(By.TAG_NAME, "h2").text.lower()
                        print(f"Section {idx} heading: {heading}")
                        if "pengalaman" in heading or "experience" in heading:
                            exp_section_idx = idx
                            break
                    except:
                        pass
            
            if not exp_section_idx:
                print("❌ Experience section not found")
                return []
            
            print(f"✓ Experience section found at index: {exp_section_idx}")
            
            # Scroll ke section experience
            try:
                exp_section = self.driver.find_element(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{exp_section_idx}]")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", exp_section)
                time.sleep(1)
            except:
                pass
            
            # Ambil list items dari experience section
            exp_items = self.driver.find_elements(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{exp_section_idx}]/div[3]/ul/li")
            print(f"Found {len(exp_items)} experience items")
            
            for idx, item in enumerate(exp_items):
                try:
                    # Strategy: ambil semua span dengan aria-hidden="true" dalam item
                    # Ini menghindari duplikasi text
                    visible_spans = item.find_elements(By.XPATH, ".//span[@aria-hidden='true']")
                    texts = []
                    
                    for span in visible_spans:
                        text = self._clean_text(span.text)
                        if text and text not in texts:  # Avoid duplicates
                            texts.append(text)
                    
                    print(f"Experience item {idx} extracted texts: {texts}")
                    
                    # LinkedIn experience pattern biasanya:
                    # [0] = Title
                    # [1] = Company · Employment type
                    # [2] = Date range
                    # [3] = Location (optional)
                    
                    if len(texts) >= 3:
                        title = texts[0]
                        company_raw = texts[1]
                        date_range = texts[2]
                        location = texts[3] if len(texts) > 3 else None
                        
                        # Parse company (remove employment type if exists)
                        # e.g., "PaperPlay Studio · Magang" -> "PaperPlay Studio"
                        company = company_raw.split('·')[0].strip() if '·' in company_raw else company_raw
                        
                        # Validasi: title dan company tidak boleh sama (indikator education)
                        if title != company:
                            exp_data = {
                                "title": title,
                                "company": company,
                                "date_range": date_range,
                                "location": location
                            }
                            experiences.append(exp_data)
                            print(f"✓ Experience {idx}: {title} at {company}")
                        else:
                            print(f"✗ Experience {idx} skipped - title == company (likely education)")
                    else:
                        print(f"✗ Experience {idx} skipped - insufficient data (only {len(texts)} fields)")
                        
                except Exception as e:
                    print(f"Error parsing experience item {idx}: {str(e)}")
                    
        except Exception as e:
            print(f"[EXTRACT_EXP] Error extracting experiences: {str(e)}")
            import traceback
            print(f"[EXTRACT_EXP] Traceback: {traceback.format_exc()}")
        
        print(f"[EXTRACT_EXP] Extraction completed. Total experiences found: {len(experiences)}")
        print(f"[EXTRACT_EXP] Experiences data: {json.dumps(experiences, indent=2, ensure_ascii=False)}\n")
        return experiences
    
    def _extract_education(self) -> List[Dict]:
        """Extract pendidikan dengan handling duplikasi LinkedIn"""
        education = []
        try:
            print(f"\n[EXTRACT_EDU] Starting education extraction...")
            
            # Wait for sections
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section"))
                )
                print("[EXTRACT_EDU] Sections loaded successfully")
            except Exception as wait_err:
                print(f"[EXTRACT_EDU] ⚠ Timeout waiting for sections: {str(wait_err)}")
            
            # Cari education section
            sections = self.driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section")
            print(f"[EXTRACT_EDU] Found {len(sections)} total sections")
            edu_section_idx = None
            
            for idx, section in enumerate(sections, start=1):
                try:
                    section_id = section.get_attribute("id")
                    if section_id and "education" in section_id.lower():
                        edu_section_idx = idx
                        break
                except:
                    pass
            
            if not edu_section_idx:
                # Fallback: cek berdasarkan heading
                for idx, section in enumerate(sections, start=1):
                    try:
                        heading = section.find_element(By.TAG_NAME, "h2").text.lower()
                        if "pendidikan" in heading or "education" in heading:
                            edu_section_idx = idx
                            break
                    except:
                        pass
            
            if not edu_section_idx:
                print("❌ Education section not found")
                return []
            
            print(f"✓ Education section found at index: {edu_section_idx}")
            
            # Scroll ke section education
            try:
                edu_section = self.driver.find_element(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{edu_section_idx}]")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", edu_section)
                time.sleep(1)
            except:
                pass
            
            # Ambil list items
            edu_items = self.driver.find_elements(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{edu_section_idx}]/div[3]/ul/li")
            print(f"Found {len(edu_items)} education items")
            
            for idx, item in enumerate(edu_items):
                try:
                    # Ambil span dengan aria-hidden="true" untuk avoid duplikasi
                    visible_spans = item.find_elements(By.XPATH, ".//span[@aria-hidden='true']")
                    texts = []
                    
                    for span in visible_spans:
                        text = self._clean_text(span.text)
                        if text and text not in texts:
                            texts.append(text)
                    
                    print(f"Education item {idx} extracted texts: {texts}")
                    
                    # LinkedIn education pattern:
                    # [0] = School name
                    # [1] = Degree / Field of study
                    # [2] = Date range
                    
                    if len(texts) >= 3:
                        school = texts[0]
                        degree = texts[1]
                        date_range = texts[2]
                        
                        # Validasi: school dan degree tidak boleh sama persis
                        if school != degree:
                            edu_data = {
                                "school": school,
                                "degree": degree,
                                "date_range": date_range
                            }
                            education.append(edu_data)
                            print(f"✓ Education {idx}: {degree} at {school}")
                        else:
                            print(f"✗ Education {idx} skipped - school == degree (malformed data)")
                    else:
                        print(f"✗ Education {idx} skipped - insufficient data (only {len(texts)} fields)")
                        
                except Exception as e:
                    print(f"Error parsing education item {idx}: {str(e)}")
                    
        except Exception as e:
            print(f"[EXTRACT_EDU] Error extracting education: {str(e)}")
            import traceback
            print(f"[EXTRACT_EDU] Traceback: {traceback.format_exc()}")
        
        print(f"[EXTRACT_EDU] Extraction completed. Total educations found: {len(education)}")
        print(f"[EXTRACT_EDU] Educations data: {json.dumps(education, indent=2, ensure_ascii=False)}\n")
        return education
    
    def _extract_certifications(self) -> List[Dict]:
        """Extract certifications dengan handling duplikasi"""
        certifications = []
        try:
            # Wait for sections
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section"))
                )
            except:
                pass
            
            # Cari certification section
            sections = self.driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section")
            cert_section_idx = None
            
            for idx, section in enumerate(sections, start=1):
                try:
                    section_id = section.get_attribute("id")
                    if section_id and ("certification" in section_id.lower() or "license" in section_id.lower()):
                        cert_section_idx = idx
                        break
                except:
                    pass
            
            if not cert_section_idx:
                # Fallback: cek berdasarkan heading
                for idx, section in enumerate(sections, start=1):
                    try:
                        heading = section.find_element(By.TAG_NAME, "h2").text.lower()
                        if "sertifikat" in heading or "license" in heading or "certification" in heading:
                            cert_section_idx = idx
                            break
                    except:
                        pass
            
            if not cert_section_idx:
                print("❌ Certifications section not found")
                return []
            
            print(f"✓ Certifications section found at index: {cert_section_idx}")
            
            # Scroll ke section certifications
            try:
                cert_section = self.driver.find_element(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{cert_section_idx}]")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cert_section)
                time.sleep(1)
            except:
                pass
            
            cert_items = self.driver.find_elements(By.XPATH, f"//*[@id='profile-content']/div/div[2]/div/div/main/section[{cert_section_idx}]/div[3]/ul/li")
            print(f"Found {len(cert_items)} certification items")
            
            for idx, item in enumerate(cert_items):
                try:
                    cert_data = {}
                    
                    # Extract name
                    try:
                        name_elem = item.find_element(By.XPATH, ".//div/div[2]/div[1]/a/div/div/div/div/span[1]")
                        cert_data["name"] = self._clean_text(name_elem.text)
                    except:
                        try:
                            name_elem = item.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                            cert_data["name"] = self._clean_text(name_elem.text)
                        except:
                            cert_data["name"] = None
                    
                    # Extract authority
                    try:
                        authority_elem = item.find_element(By.XPATH, ".//div/div[2]/div[1]/a/span[1]/span[1]")
                        cert_data["authority"] = self._clean_text(authority_elem.text)
                    except:
                        cert_data["authority"] = None
                    
                    # Extract issued date
                    try:
                        issued_elem = item.find_element(By.XPATH, ".//div/div[2]/div[1]/a/span[2]/span[1]")
                        cert_data["issued"] = self._clean_text(issued_elem.text)
                    except:
                        cert_data["issued"] = None
                    
                    # Extract credential ID
                    try:
                        credential_elem = item.find_element(By.XPATH, ".//div/div[2]/div[1]/a/span[3]/span[1]")
                        cert_data["credential_id"] = self._clean_text(credential_elem.text)
                    except:
                        cert_data["credential_id"] = None
                    
                    # Hanya tambahkan jika ada name
                    if cert_data.get("name"):
                        certifications.append(cert_data)
                        print(f"✓ Certification {idx}: {cert_data['name']}")
                    else:
                        print(f"✗ Certification {idx} skipped - no name found")
                        
                except Exception as e:
                    print(f"Error parsing certification item {idx}: {str(e)}")
                    
        except Exception as e:
            print(f"Error extracting certifications: {str(e)}")
        
        return certifications
    
    def _generate_skills_with_ai(self, headline: str, about: str, experiences: List[Dict]) -> str:
        """Generate skills menggunakan Gemini API berdasarkan headline, about, dan experience"""
        try:
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                print("⚠ GEMINI_API_KEY tidak diset, skip AI generation")
                return ""
            
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Siapkan context dari experiences
            experience_text = ""
            if experiences:
                for exp in experiences[:5]:  # Ambil 5 experience terakhir
                    exp_text = f"- {exp.get('title', '')}"
                    if exp.get('company'):
                        exp_text += f" di {exp['company']}"
                    if exp.get('description'):
                        exp_text += f": {exp['description'][:100]}"
                    experience_text += exp_text + "\n"
            
            # Buat prompt untuk Gemini
            prompt = f"""Based on the following LinkedIn profile information, generate a list of relevant skills.

Headline: {headline}

About: {about}

Experience:
{experience_text}

Provide the response in the format: skill1|skill2|skill3|skill4|skill5

Only include relevant and specific skills, with no additional explanation. Maximum 10 skills."""
            
            print("[AI] Generating skills dengan Gemini...")
            response = model.generate_content(prompt)
            
            if response.text:
                skills_text = response.text.strip()
                print(f"[AI] Generated skills: {skills_text}")
                return skills_text
            else:
                print("[AI] Gemini response kosong")
                return ""
                
        except Exception as e:
            print(f"[AI ERROR] Error generating skills: {str(e)}")
            return ""
    
    def _extract_skills(self) -> str:
        """Extract skills dari halaman details/skills/"""
        skills = []
        try:
            profile_url = self.driver.current_url
            skills_url = profile_url.rstrip("/") + "/details/skills/"
            self.driver.get(skills_url)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'pvs-list__container')]"))
                )
            except:
                time.sleep(2)

            # Ambil hanya span dengan aria-hidden="true" untuk avoid duplikasi
            skill_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'pvs-list__container')]//li//span[@aria-hidden='true']")
            
            for elem in skill_elements:
                skill_text = self._clean_text(elem.text)
                # Filter: hanya ambil skill (biasanya pendek, < 50 karakter)
                # Skip yang panjang (biasanya endorsement info)
                if skill_text and len(skill_text) < 50 and skill_text not in skills:
                    skills.append(skill_text)
            
            print(f"Extracted {len(skills)} skills")
            return "|".join(skills) if skills else ""
            
        except Exception as e:
            print(f"Error extracting skills: {str(e)}")
            return ""
