#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import urllib.request
import urllib.error
import base64
import ssl
from datetime import datetime

class CampaignSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campaign Setup Automator - RTB House (Enriched)")
        
        # Pobierz rozdzielczość ekranu
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Ustaw okno na 80% rozmiaru ekranu
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Wyśrodkuj okno
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Minimalny rozmiar żeby nie było za małe
        self.root.minsize(1400, 900)
        
        # Opcjonalnie: maksymalizuj przy starcie
        # self.root.state('zoomed')
        
        # API configuration
        self.api_url = "https://api.campaigns.rtbhouse.biz/api/campaigns/graphql"
        self.auth = {
            "username": "ei-inv-graphql-campaigns-api",
            "password": "KcyBKW283cTXTuiW"
        }
        
        self.selected_fields = set()
        self.health_check_passed = False
        
        # Słownik z podpowiedziami dla pól
        self.field_hints = {
            "supportedAdApiFrameworks": "OMID_1, VPAID_1_0, VPAID_2_0",
            "allowedProfileIdentifierTypes": "aaid, idfa, idfv, rtbhcookie",
            "notAllowedProfileIdentifierTypes": "aaid, idfa, idfv, rtbhcookie",
            "fullscreenMobilePlacement": "ONLY_REWARDED, ONLY_INTERSTITIAL, ONLY_REWARDED_AND_INTERSTITIAL, REWARDED_AND_INTERSTITIAL_NOT_ALLOWED",
            "allowedDeviceTypes": "UNKNOWN, PC, MOBILE, PHONE, TABLET, TV, GAME_CONSOLE, OTHER",
            "notAllowedDeviceTypes": "UNKNOWN, PC, MOBILE, PHONE, TABLET, TV, GAME_CONSOLE, OTHER",
            "allowedPlacementEnvironments": "HTTP, AAID, IDFA, OTHER",
            "notAllowedPlacementEnvironments": "HTTP, AAID, IDFA, OTHER",
            "startDate": "Format: YYYY-MM-DD (np. 2024-01-15)",
            "endDate": "Format: YYYY-MM-DD (np. 2024-12-31)",
            "dailyBudget": "Wartość liczbowa (np. 100.50)",
            "monthlyBudget": "Wartość liczbowa (np. 3000.00)",
            "dailyImpressions": "Wartość liczbowa (np. 1000000)",
            "monthlyImpressions": "Wartość liczbowa (np. 30000000)",
            "cpmVisitors": "Wartość liczbowa CPM (np. 0.50)",
            "cpmShoppers": "Wartość liczbowa CPM (np. 1.20)",
            "cpmBuyers": "Wartość liczbowa CPM (np. 2.00)",
            "cpmNew": "Wartość liczbowa CPM (np. 0.80)",
            "allowedCountries": "Kody krajów oddzielone przecinkami (np. PL,US,DE)",
            "excludedCountries": "Kody krajów oddzielone przecinkami (np. CN,RU)",
            "includedRegions": "Regiony oddzielone przecinkami",
            "includedCitiesCity": "Miasta oddzielone przecinkami",
            "allowedSSPs": "Nazwy SSP oddzielone przecinkami",
            "notAllowedSSPs": "Nazwy SSP oddzielone przecinkami",
            "allowedHosts": "Domeny oddzielone przecinkami (np. example.com,test.com)",
            "notAllowedHosts": "Domeny oddzielone przecinkami",
            "forbiddenUrlLabels": "Etykiety URL oddzielone przecinkami",
            "allowedAppIds": "ID aplikacji oddzielone przecinkami",
            "notAllowedAppIds": "ID aplikacji oddzielone przecinkami",
            "creativeIds": "ID kreatyw oddzielone przecinkami",
            "allowedDeals": "ID dealów oddzielone przecinkami",
            "notAllowedDeals": "ID dealów oddzielone przecinkami"
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Stylizacja głównego okna
        self.root.configure(bg='#f0f0f0')
        
        # Style dla ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Konfiguracja kolorów
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', padding=[10, 5])
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Health Check Tab
        self.health_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.health_frame, text="Health check")
        self.setup_health_check_tab()
        
        # Campaign Setup Tab
        self.campaign_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.campaign_frame, text="Konfiguracja kampanii")
        self.setup_campaign_tab()
        
        # Campaign Check Tab (NOWA)
        self.check_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.check_frame, text="Sprawdzenie setupu kampanii")
        self.setup_campaign_check_tab()
        
        # Status Change Tab
        self.status_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.status_frame, text="Zmiana statusu")
        self.setup_status_tab()
        
        # Initially disable other tabs
        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")
        self.notebook.tab(3, state="disabled")
        
        # Dodaj przyciski do zmiany rozmiaru (opcjonalnie)
        size_frame = ttk.Frame(self.root)
        size_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        
        ttk.Button(size_frame, text="Małe okno", 
                  command=lambda: self.root.geometry("1200x800")).pack(side="left", padx=5)
        ttk.Button(size_frame, text="Średnie okno", 
                  command=lambda: self.root.geometry("1600x1000")).pack(side="left", padx=5)
        ttk.Button(size_frame, text="Duże okno", 
                  command=lambda: self.root.geometry("2000x1400")).pack(side="left", padx=5)
        ttk.Button(size_frame, text="Pełny ekran", 
                  command=lambda: self.root.state('zoomed')).pack(side="left", padx=5)

    def setup_health_check_tab(self):
        # Header
        header_frame = ttk.Frame(self.health_frame)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header_frame, text="Health check advertisera", 
                  font=('Arial', 16, 'bold')).pack()
        ttk.Label(header_frame, text="Sprawdź dostępność i konfigurację advertisera", 
                  font=('Arial', 10), foreground='gray').pack()
        
        # Input section
        input_frame = ttk.LabelFrame(self.health_frame, text="Dane wejściowe", padding=15)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(input_frame, text="Advertiser ID:").pack(anchor="w")
        self.advertiser_id_var = tk.StringVar(value="63113")
        advertiser_entry = ttk.Entry(input_frame, textvariable=self.advertiser_id_var, 
                                    width=20, font=('Arial', 11))
        advertiser_entry.pack(pady=5)
        
        # Button with icon
        ttk.Button(input_frame, text="Sprawdź advertisera", 
                  command=self.run_health_check).pack(pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(self.health_frame, text="Wyniki", padding=15)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.health_results = scrolledtext.ScrolledText(results_frame, height=20, width=80,
                                                       font=('Consolas', 9))
        self.health_results.pack(fill="both", expand=True)

    def setup_campaign_check_tab(self):
        # Header
        header_frame = ttk.Frame(self.check_frame)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(header_frame, text="Sprawdzenie setupu kampanii", 
                  font=('Arial', 16, 'bold')).pack()
        ttk.Label(header_frame, text="Sprawdź aktualną konfigurację kampanii i porównaj z oczekiwanymi wartościami", 
                  font=('Arial', 10), foreground='gray').pack()
        
        # Input section
        input_frame = ttk.LabelFrame(self.check_frame, text="Dane wejściowe", padding=15)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Campaign ID input
        ttk.Label(input_frame, text="Campaign ID:").pack(anchor="w")
        self.check_campaign_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.check_campaign_id_var, width=20).pack(pady=5)
        
        # Advertiser ID input
        ttk.Label(input_frame, text="Advertiser ID:").pack(anchor="w", pady=(10, 0))
        self.check_advertiser_id_var = tk.StringVar(value="63113")
        ttk.Entry(input_frame, textvariable=self.check_advertiser_id_var, width=20).pack(pady=5)
        
        # Field selection
        ttk.Label(input_frame, text="Wybierz pola do sprawdzenia:").pack(pady=(20, 5))
        
        # Create scrollable frame for checkboxes
        canvas = tk.Canvas(input_frame, height=200)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Field checkboxes for campaign check
        self.check_field_vars = {}
        self.expected_value_vars = {}  # NOWE: słownik dla oczekiwanych wartości
        check_fields = [
            # Podstawowe informacje
            ("campaign_name", "Nazwa kampanii"),
            ("campaign_status", "Status kampanii"),
            ("startDate", "startDate"),
            ("endDate", "endDate"),
            ("subcampaignType", "subcampaignType"),
            ("dataCenters", "dataCenters"),
            ("landing_url", "Landing URL"),
            
            # Budżety i limity
            ("dailyBudget", "dailyBudget"),
            ("monthlyBudget", "monthlyBudget"),
            ("dailyImpressions", "dailyImpressions"),
            ("monthlyImpressions", "monthlyImpressions"),
            ("spendDaily", "spendDaily"),
            ("userImpressionsDaily", "userImpressionsDaily"),
            
            # Targeting Policy
            ("allowedSSPs", "allowedSSPs"),
            ("notAllowedSSPs", "notAllowedSSPs"),
            ("allowedDeals", "allowedDeals"),
            ("notAllowedDeals", "notAllowedDeals"),
            ("allowedHosts", "allowedHosts"),
            ("notAllowedHosts", "notAllowedHosts"),
            ("allowedAppIds", "allowedAppIds"),
            ("notAllowedAppIds", "notAllowedAppIds"),
            ("forbiddenUrlLabels", "forbiddenUrlLabels"),
            ("requiredUrlLabels", "requiredUrlLabels"),
            
            # Ad API Framework
            ("supportedAdApiFrameworks", "supportedAdApiFrameworks"),
            
            # Profile Identifiers
            ("allowedProfileIdentifierTypes", "allowedProfileIdentifierTypes"),
            ("notAllowedProfileIdentifierTypes", "notAllowedProfileIdentifierTypes"),
            
            # Mobile placement
            ("fullscreenMobilePlacement", "fullscreenMobilePlacement"),
            
            # Bidding Model CPM
            ("cpmVisitors", "cpmVisitors"),
            ("cpmShoppers", "cpmShoppers"),
            ("cpmBuyers", "cpmBuyers"),
            ("cpmNew", "cpmNew"),
            
            # Device Types
            ("allowedDeviceTypes", "allowedDeviceTypes"),
            ("notAllowedDeviceTypes", "notAllowedDeviceTypes"),
            
            # Geotargeting
            ("includedCountries", "includedCountries"),
            ("excludedCountries", "excludedCountries"),
            ("includedRegions", "includedRegions"),
            ("includedCities", "includedCities"),
            
            # User Segments
            ("userSegments", "userSegments"),
            ("allowOneTagBids", "allowOneTagBids"),
            
            # Creative IDs
            ("creativeIds", "creativeIds"),
            
            # Placement Environment
            ("allowedPlacementEnvironments", "allowedPlacementEnvironments"),
            ("notAllowedPlacementEnvironments", "notAllowedPlacementEnvironments"),
            
            # Traffic Quality
            ("maxBR", "maxBR"),
            ("minVCR", "minVCR"),
            ("minViewability", "minViewability"),
            ("allowedNulls", "allowedNulls"),
            
            # Cookie Types
            ("allowedCookieTypes", "allowedCookieTypes"),
            
            # Fraud Prevention
            ("forbiddenFraudPreventionLabels", "forbiddenFraudPreventionLabels"),
        ]
        
        for field_id, field_label in check_fields:
            # Checkbox dla pola
            var = tk.BooleanVar()
            self.check_field_vars[field_id] = var
            cb = ttk.Checkbutton(scrollable_frame, text=field_label, variable=var,
                               command=lambda f=field_id: self.update_expected_value_field(f))
            cb.pack(anchor="w", padx=5, pady=2)
            
            # Entry dla oczekiwanej wartości
            expected_var = tk.StringVar()
            self.expected_value_vars[field_id] = expected_var
            expected_entry = ttk.Entry(scrollable_frame, textvariable=expected_var, 
                                     width=30, state="disabled")
            expected_entry.pack(anchor="w", padx=25, pady=1)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Button to check campaign
        ttk.Button(input_frame, text=" Sprawdź setup kampanii", 
                  command=self.check_campaign_setup).pack(pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(self.check_frame, text="Wyniki sprawdzenia", padding=15)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.check_results = scrolledtext.ScrolledText(results_frame, height=25, width=100,
                                                      font=('Consolas', 9))
        self.check_results.pack(fill="both", expand=True)

    def update_expected_value_field(self, field_id):
        """Włącza/wyłącza pole oczekiwanej wartości w zależności od checkboxa"""
        expected_entry = None
        # Znajdź odpowiednie pole entry
        for widget in self.check_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "Dane wejściowe":
                for child in widget.winfo_children():
                    if isinstance(child, tk.Canvas):
                        for canvas_child in child.winfo_children():
                            if isinstance(canvas_child, ttk.Frame):
                                for entry_widget in canvas_child.winfo_children():
                                    if isinstance(entry_widget, ttk.Entry) and entry_widget.cget("textvariable") == str(self.expected_value_vars[field_id]):
                                        expected_entry = entry_widget
                                        break
        
        if expected_entry:
            if self.check_field_vars[field_id].get():
                expected_entry.config(state="normal")
            else:
                expected_entry.config(state="disabled")

    def get_expected_value(self, field_name):
        """Pobiera oczekiwaną wartość dla pola z interfejsu użytkownika"""
        expected_value = self.expected_value_vars.get(field_name, tk.StringVar()).get()
        return expected_value.strip() if expected_value.strip() else None

    def setup_campaign_tab(self):
        # Campaign ID input
        ttk.Label(self.campaign_frame, text="Campaign ID:").pack(pady=5)
        self.campaign_id_var = tk.StringVar()
        ttk.Entry(self.campaign_frame, textvariable=self.campaign_id_var, width=20).pack(pady=5)
        
        # Field selection
        ttk.Label(self.campaign_frame, text="Wybierz pola do konfiguracji:").pack(pady=(20, 5))
        
        # Create scrollable frame for checkboxes
        canvas = tk.Canvas(self.campaign_frame)
        scrollbar = ttk.Scrollbar(self.campaign_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Field checkboxes
        self.field_vars = {}
        fields = [
            # Podstawowe informacje
            ("startDate", "Data rozpoczęcia"),
            ("endDate", "Data zakończenia"),
            
            # Budżety
            ("dailyBudget", "dailyBudget"),
            ("monthlyBudget", "monthlyBudget"),
            ("dailyImpressions", "dailyImpressions"),
            ("monthlyImpressions", "monthlyImpressions"),
            
            # Targeting Policy - Deals
            ("allowedDeals", "allowedDeals"),
            ("notAllowedDeals", "notAllowedDeals"),
            
            # Ad API Framework
            ("supportedAdApiFrameworks", "supportedAdApiFrameworks"),
            
            # Profile Identifiers
            ("allowedProfileIdentifierTypes", "allowedProfileIdentifierTypes"),
            ("notAllowedProfileIdentifierTypes", "notAllowedProfileIdentifierTypes"),
            
            # Mobile placement
            ("fullscreenMobilePlacement", "fullscreenMobilePlacement"),
            
            # Bidding Model CPM
            ("cpmVisitors", "cpmVisitors"),
            ("cpmShoppers", "cpmShoppers"),
            ("cpmBuyers", "cpmBuyers"),
            ("cpmNew", "cpmNew"),
            
            # Device Types
            ("allowedDeviceTypes", "allowedDeviceTypes"),
            ("notAllowedDeviceTypes", "notAllowedDeviceTypes"),
            
            # Geotargeting
            ("includedCountriesCountry", "includedCountriesCountry"),
            ("excludedCountries", "excludedCountries"),
            ("includedRegions", "includedRegions"),
            ("includedCitiesCity", "includedCitiesCity"),
            
            # SSP Policy
            ("notAllowedSSPs", "notAllowedSSPs"),
            ("allowedSSPs", "allowedSSPs"),
            
            # Creative IDs
            ("creativeIds", "creativeIds"),
            
            # Placement Environment
            ("allowedPlacementEnvironments", "allowedPlacementEnvironments"),
            ("notAllowedPlacementEnvironments", "notAllowedPlacementEnvironments"),
        ]
        
        for field_id, field_label in fields:
            var = tk.BooleanVar()
            self.field_vars[field_id] = var
            cb = ttk.Checkbutton(scrollable_frame, text=field_label, variable=var,
                               command=self.update_field_config)
            cb.pack(anchor="w", padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Field configuration area
        ttk.Label(self.campaign_frame, text="Konfiguracja wybranych pól:").pack(pady=(20, 5))
        self.field_config_frame = ttk.Frame(self.campaign_frame)
        self.field_config_frame.pack(fill="both", expand=True, padx=10)
        
        # Save button
        ttk.Button(self.campaign_frame, text="Zapisz konfigurację", 
                  command=self.save_campaign_config).pack(pady=10)
    
    def setup_status_tab(self):
        # Campaign ID input
        ttk.Label(self.status_frame, text="ID Kampanii:").pack(pady=5)
        self.status_campaign_id_var = tk.StringVar()
        ttk.Entry(self.status_frame, textvariable=self.status_campaign_id_var, width=20).pack(pady=5)
        
        # Status selection
        ttk.Label(self.status_frame, text="Nowy Status:").pack(pady=(20, 5))
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(self.status_frame, textvariable=self.status_var, 
                                   values=["ACTIVE", "PAUSED"], state="readonly")
        status_combo.pack(pady=5)
        
        # Comment
        ttk.Label(self.status_frame, text="Komentarz:").pack(pady=(20, 5))
        self.comment_text = scrolledtext.ScrolledText(self.status_frame, height=5, width=60)
        self.comment_text.pack(pady=5, padx=10)
        
        # Change status button
        ttk.Button(self.status_frame, text="Zmień status", 
                  command=self.change_campaign_status).pack(pady=10)

    def update_field_config(self):
        # Clear previous config
        for widget in self.field_config_frame.winfo_children():
            widget.destroy()
        
        # Add config for selected fields
        row = 0
        for field_id, var in self.field_vars.items():
            if var.get():
                # Label z nazwą pola
                ttk.Label(self.field_config_frame, text=f"{field_id}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
                
                # Entry field
                entry = ttk.Entry(self.field_config_frame, width=40)
                entry.grid(row=row, column=1, padx=5, pady=2)
                
                # Label z podpowiedzią
                if field_id in self.field_hints:
                    hint_label = ttk.Label(self.field_config_frame, 
                                         text=f"Podpowiedź: {self.field_hints[field_id]}",
                                         foreground="gray", 
                                         font=("TkDefaultFont", 8))
                    hint_label.grid(row=row, column=2, sticky="w", padx=5, pady=2)
                
                row += 1

    def check_campaign_setup(self):
        campaign_id = self.check_campaign_id_var.get()
        advertiser_id = self.check_advertiser_id_var.get()
        
        if not campaign_id or not advertiser_id:
            messagebox.showerror("Błąd", "Wprowadź ID kampanii i advertisera")
            return
        
        selected_fields = [field_id for field_id, var in self.check_field_vars.items() if var.get()]
        if not selected_fields:
            messagebox.showerror("Błąd", "Wybierz przynajmniej jedno pole do sprawdzenia")
            return
        
        self.check_results.delete(1.0, tk.END)
        self.check_results.insert(tk.END, "Sprawdzanie setupu kampanii...\n")
        self.root.update()
        
        try:
            # Pobierz dane kampanii
            campaign_data = self.get_campaign_data(int(advertiser_id), int(campaign_id))
            
            if campaign_data:
                self.display_campaign_check_results(campaign_data, selected_fields)
            else:
                self.check_results.insert(tk.END, "Nie znaleziono kampanii o podanym ID\n")
                
        except Exception as e:
            self.check_results.insert(tk.END, f"Błąd: {str(e)}\n")
            messagebox.showerror("Błąd", f"Błąd podczas sprawdzania kampanii: {str(e)}")

    def get_campaign_data(self, advertiser_id, campaign_id):
        """Pobiera szczegółowe dane kampanii używając zapytania z get-campaign-info.md"""
        query = """
            query GetSubcampaignOverview($advertiserId: Int!, $subcampaignId: Int!) {
                advertiser(advertiserId: $advertiserId) {
                    advertiserId
                    subcampaign(subcampaignId: $subcampaignId) {
                        subcampaignId
                        basicInfo {
                            name
                            labels
                        }
                        campaignStatus {
                            startDate
                            endDate
                            status {
                                value
                            }
                        }
                        properties {
                            subcampaignType
                            dataCenters
                        }
                        landingMacro {
                            defaultUrl {
                                url
                            }
                        }
                        limits {
                            budget {
                                daily
                                monthly
                            }
                            events {
                                impressions {
                                    daily
                                    monthly
                                }
                            }
                        }
                        biddingModel {
                            cpm {
                                visitors
                                shoppers
                                buyers
                                new
                            }
                        }
                        targetingPolicy {
                            sspPolicy {
                                allowedSsps
                                notAllowedSsps
                            }
                            dealPolicy {
                                allowedDeals {
                                    id
                                    identifier
                                }
                                notAllowedDeals {
                                    id
                                    identifier
                                }
                            }
                            userPolicy {
                                allowOneTagBids
                                userSegments
                                profileIdentifiers {
                                    allowedProfileIdentifierTypes
                                    notAllowedProfileIdentifierTypes
                                }
                            }
                            deviceTypePolicy {
                                allowedDeviceTypes
                                notAllowedDeviceTypes
                            }
                            placementEnvironmentPolicy {
                                allowedPlacementEnvironments
                                notAllowedPlacementEnvironments
                            }
                            adApiFrameworkPolicy {
                                supportedAdApiFrameworks
                            }
                            inAppsPolicy {
                                fullscreenMobilePlacement
                            }
                        }
                        geotargeting {
                            includedCountries {
                                country
                                includedRegions
                                includedCities {
                                    city
                                }
                            }
                            excludedCountries
                        }
                        creatives {
                            creativeId
                        }
                        trafficQuality {
                            maxBr
                            video {
                                minVcr
                            }
                            viewability {
                                minValue
                                allowUnknown
                            }
                        }
                    }
                }
            }
        """
        
        try:
            response = self.make_graphql_request(query, {
                "advertiserId": advertiser_id,
                "subcampaignId": campaign_id
            })
            
            # POPRAWKA: Sprawdź czy response nie jest None i czy ma odpowiednią strukturę
            if response and response.get("data") and response["data"].get("advertiser"):
                subcampaign = response["data"]["advertiser"].get("subcampaign")
                if subcampaign:
                    return subcampaign
                else:
                    self.check_results.insert(tk.END, f"Kampania o ID {campaign_id} nie została znaleziona w advertiserze {advertiser_id}\n")
                    return None
            else:
                error_msg = "Nie udało się pobrać danych kampanii"
                if response and response.get("errors"):
                    error_msg += f": {response['errors']}"
                self.check_results.insert(tk.END, f"{error_msg}\n")
                return None
                
        except Exception as e:
            self.check_results.insert(tk.END, f"Błąd podczas pobierania danych: {str(e)}\n")
            return None

    def display_campaign_check_results(self, campaign_data, selected_fields):
        """Wyświetla wyniki sprawdzenia setupu kampanii"""
        self.check_results.delete(1.0, tk.END)
        
        # POPRAWKA: Sprawdź czy campaign_data nie jest None
        if not campaign_data:
            self.check_results.insert(tk.END, "Brak danych kampanii do wyświetlenia\n")
            return
        
        self.check_results.insert(tk.END, f"Wyniki sprawdzenia setupu kampanii ID: {campaign_data.get('subcampaignId', 'N/A')}\n")
        self.check_results.insert(tk.END, "=" * 80 + "\n\n")
        
        # Mapowanie pól na dane z GraphQL z dodatkowymi zabezpieczeniami
        field_mapping = {
            "campaign_name": self.safe_get(campaign_data, ["basicInfo", "name"]),
            "campaign_status": self.safe_get(campaign_data, ["campaignStatus", "status", "value"]),
            "startDate": self.safe_get(campaign_data, ["campaignStatus", "startDate"]),
            "endDate": self.safe_get(campaign_data, ["campaignStatus", "endDate"]),
            "subcampaignType": self.safe_get(campaign_data, ["properties", "subcampaignType"]),
            "dataCenters": self.safe_join(self.safe_get(campaign_data, ["properties", "dataCenters"])),
            "landing_url": self.safe_get(campaign_data, ["landingMacro", "defaultUrl", "url"]),
            "dailyBudget": self.safe_get(campaign_data, ["limits", "budget", "daily"]),
            "monthlyBudget": self.safe_get(campaign_data, ["limits", "budget", "monthly"]),
            "dailyImpressions": self.safe_get(campaign_data, ["limits", "events", "impressions", "daily"]),
            "monthlyImpressions": self.safe_get(campaign_data, ["limits", "events", "impressions", "monthly"]),
            "cpmVisitors": self.safe_get(campaign_data, ["biddingModel", "cpm", "visitors"]),
            "cpmShoppers": self.safe_get(campaign_data, ["biddingModel", "cpm", "shoppers"]),
            "cpmBuyers": self.safe_get(campaign_data, ["biddingModel", "cpm", "buyers"]),
            "cpmNew": self.safe_get(campaign_data, ["biddingModel", "cpm", "new"]),
            "allowedSSPs": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "sspPolicy", "allowedSsps"])),
            "notAllowedSSPs": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "sspPolicy", "notAllowedSsps"])),
            "allowedDeals": self.safe_join_deals(self.safe_get(campaign_data, ["targetingPolicy", "dealPolicy", "allowedDeals"])),
            "notAllowedDeals": self.safe_join_deals(self.safe_get(campaign_data, ["targetingPolicy", "dealPolicy", "notAllowedDeals"])),
            "supportedAdApiFrameworks": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "adApiFrameworkPolicy", "supportedAdApiFrameworks"])),
            "allowedProfileIdentifierTypes": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "userPolicy", "profileIdentifiers", "allowedProfileIdentifierTypes"])),
            "notAllowedProfileIdentifierTypes": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "userPolicy", "profileIdentifiers", "notAllowedProfileIdentifierTypes"])),
            "fullscreenMobilePlacement": self.safe_get(campaign_data, ["targetingPolicy", "inAppsPolicy", "fullscreenMobilePlacement"]),
            "allowedDeviceTypes": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "deviceTypePolicy", "allowedDeviceTypes"])),
            "notAllowedDeviceTypes": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "deviceTypePolicy", "notAllowedDeviceTypes"])),
            "includedCountries": self.safe_join_countries(self.safe_get(campaign_data, ["geotargeting", "includedCountries"])),
            "excludedCountries": self.safe_join(self.safe_get(campaign_data, ["geotargeting", "excludedCountries"])),
            "includedRegions": self.safe_join_regions(self.safe_get(campaign_data, ["geotargeting", "includedCountries"])),
            "includedCities": self.safe_join_cities(self.safe_get(campaign_data, ["geotargeting", "includedCountries"])),
            "userSegments": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "userPolicy", "userSegments"])),
            "allowOneTagBids": self.safe_get(campaign_data, ["targetingPolicy", "userPolicy", "allowOneTagBids"]),
            "creativeIds": self.safe_join_creatives(self.safe_get(campaign_data, ["creatives"])),
            "allowedPlacementEnvironments": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "placementEnvironmentPolicy", "allowedPlacementEnvironments"])),
            "notAllowedPlacementEnvironments": self.safe_join(self.safe_get(campaign_data, ["targetingPolicy", "placementEnvironmentPolicy", "notAllowedPlacementEnvironments"])),
            "maxBR": self.safe_get(campaign_data, ["trafficQuality", "maxBr"]),
            "minVCR": self.safe_get(campaign_data, ["trafficQuality", "video", "minVcr"]),
            "minViewability": self.safe_get(campaign_data, ["trafficQuality", "viewability", "minValue"]),
            "allowedNulls": self.safe_get(campaign_data, ["trafficQuality", "viewability", "allowUnknown"]),
        }
        
        for field_name in selected_fields:
            actual_value = field_mapping.get(field_name, "N/A")
            if actual_value is None:
                actual_value = "N/A"
            
            # Sprawdź czy użytkownik podał oczekiwaną wartość
            expected_value = self.get_expected_value(field_name)
            
            self.check_results.insert(tk.END, f"{field_name:35}: {actual_value}\n")
            
            if expected_value:
                status = self.compare_values(actual_value, expected_value)
                self.check_results.insert(tk.END, f"{'':35}  Status: {status}\n")
                self.check_results.insert(tk.END, f"{'':35}  Oczekiwane: {expected_value}\n")
            else:
                self.check_results.insert(tk.END, f"{'':35}  (Brak oczekiwanej wartości)\n")
            
            self.check_results.insert(tk.END, "\n")

    def safe_get(self, data, keys):
        """Bezpieczne pobieranie zagnieżdżonych wartości z słownika"""
        try:
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current
        except (TypeError, KeyError, AttributeError):
            return None

    def safe_join(self, data, separator=", "):
        """Bezpieczne łączenie listy w string"""
        if data is None:
            return "N/A"
        if isinstance(data, list):
            return separator.join(str(item) for item in data if item is not None)
        return str(data) if data is not None else "N/A"

    def safe_join_deals(self, deals_data):
        """Bezpieczne łączenie dealów"""
        if deals_data is None:
            return "N/A"
        if isinstance(deals_data, list):
            identifiers = []
            for deal in deals_data:
                if isinstance(deal, dict) and "identifier" in deal:
                    identifiers.append(deal["identifier"])
                elif isinstance(deal, str):
                    identifiers.append(deal)
            return ", ".join(identifiers) if identifiers else "N/A"
        return str(deals_data) if deals_data is not None else "N/A"

    def safe_join_countries(self, countries_data):
        """Bezpieczne łączenie krajów"""
        if countries_data is None:
            return "N/A"
        if isinstance(countries_data, list):
            countries = []
            for country in countries_data:
                if isinstance(country, dict) and "country" in country:
                    countries.append(country["country"])
                elif isinstance(country, str):
                    countries.append(country)
            return ", ".join(countries) if countries else "N/A"
        return str(countries_data) if countries_data is not None else "N/A"

    def safe_join_regions(self, countries_data):
        """Bezpieczne łączenie regionów"""
        if countries_data is None:
            return "N/A"
        if isinstance(countries_data, list):
            regions = []
            for country in countries_data:
                if isinstance(country, dict) and "includedRegions" in country:
                    if isinstance(country["includedRegions"], list):
                        regions.extend(country["includedRegions"])
            return ", ".join(regions) if regions else "N/A"
        return "N/A"

    def safe_join_cities(self, countries_data):
        """Bezpieczne łączenie miast"""
        if countries_data is None:
            return "N/A"
        if isinstance(countries_data, list):
            cities = []
            for country in countries_data:
                if isinstance(country, dict) and "includedCities" in country:
                    if isinstance(country["includedCities"], list):
                        for city in country["includedCities"]:
                            if isinstance(city, dict) and "city" in city:
                                cities.append(city["city"])
                            elif isinstance(city, str):
                                cities.append(city)
            return ", ".join(cities) if cities else "N/A"
        return "N/A"

    def safe_join_creatives(self, creatives_data):
        """Bezpieczne łączenie kreacji"""
        if creatives_data is None:
            return "N/A"
        if isinstance(creatives_data, list):
            creative_ids = []
            for creative in creatives_data:
                if isinstance(creative, dict) and "creativeId" in creative:
                    creative_ids.append(str(creative["creativeId"]))
                elif isinstance(creative, (str, int)):
                    creative_ids.append(str(creative))
            return ", ".join(creative_ids) if creative_ids else "N/A"
        return str(creatives_data) if creatives_data is not None else "N/A"

    def compare_values(self, actual, expected):
        """Porównuje rzeczywistą wartość z oczekiwaną"""
        if actual == expected:
            return "✅ PASUJE"
        elif str(actual).lower() in str(expected).lower() or str(expected).lower() in str(actual).lower():
            return "⚠️ CZĘŚCIOWO PASUJE"
        else:
            return "❌ NIE PASUJE"

    def run_health_check(self):
        advertiser_id = self.advertiser_id_var.get()
        if not advertiser_id:
            messagebox.showerror("Błąd", "Wprowadź ID advertisera")
            return
        
        self.health_results.delete(1.0, tk.END)
        self.health_results.insert(tk.END, "Sprawdzanie advertisera...\n")
        self.root.update()
        
        try:
            query = """
                query GetAdvertiserData($advertiserId: Int!) {
                    advertiser(advertiserId: $advertiserId) {
                        advertiserId
                        info {
                            url
                            campaignType
                            currency
                            labels
                        }
                        basicInfo {
                            profitCenter
                            country
                            languages
                            timezone
                        }
                        businessInfo {
                            agency
                            brand
                            businessType
                        }
                        accessPolicyGroups
                        conversionTracking {
                            deduplication
                        }
                        technical {
                            traffic {
                                defaultSubcampaignDataCenters
                            }
                            visibilities {
                                hasSegmentNew
                            }
                        }
                        biddingModel {
                            cpm {
                                visitors
                                shoppers
                                buyers
                                new
                            }
                        }
                        targetingPolicy {
                            sspPolicy {
                                allowedSsps
                                notAllowedSsps
                            }
                        }
                    }
                }
            """
            
            response = self.make_graphql_request(query, {"advertiserId": int(advertiser_id)})
            
            if response.get("data") and response["data"].get("advertiser"):
                self.display_health_check_results(response["data"]["advertiser"])
                self.health_check_passed = True
                self.notebook.tab(1, state="normal")
                self.notebook.tab(2, state="normal")
                self.notebook.tab(3, state="normal")
                messagebox.showinfo("Sukces", "Health check zakończony pomyślnie!")
            else:
                self.health_results.insert(tk.END, "Nie znaleziono advertisera o podanym ID\n")
                
        except Exception as e:
            self.health_results.insert(tk.END, f"Błąd: {str(e)}\n")
            messagebox.showerror("Błąd", f"Błąd podczas sprawdzania advertisera: {str(e)}")
    
    def display_health_check_results(self, advertiser):
        self.health_results.delete(1.0, tk.END)
        
        expected_values = {
            "URL": "https://rtbhouse.com/",
            "type": "PERFORMANCE",
            "profit center": "LAB",
            "country": "PL",
            "currency": "USD",
            "languages": "Polish, English (US)",
            "labels": "",
            "timezone": "Europe/Warsaw",
            "agency": "DIRECT",
            "brand": "RTBHouse",
            "business type": "other",
            "access policy groups": "AI Marketing LAB",
            "deduplication": "DEFAULT",
            "data centers": "ams, ash, sin, phx",
            "has_segment_new": "TRUE"
        }
        
        self.health_results.insert(tk.END, f"Wyniki health check dla advertiser ID: {advertiser['advertiserId']}\n")
        self.health_results.insert(tk.END, "=" * 60 + "\n\n")
        
        fields = [
            ("URL", advertiser.get("info", {}).get("url")),
            ("type", advertiser.get("info", {}).get("campaignType")),
            ("profit center", advertiser.get("basicInfo", {}).get("profitCenter")),
            ("country", advertiser.get("basicInfo", {}).get("country")),
            ("currency", advertiser.get("info", {}).get("currency")),
            ("languages", ", ".join(advertiser.get("basicInfo", {}).get("languages", []))),
            ("labels", ", ".join(advertiser.get("info", {}).get("labels", []))),
            ("timezone", advertiser.get("basicInfo", {}).get("timezone")),
            ("agency", advertiser.get("businessInfo", {}).get("agency")),
            ("brand", advertiser.get("businessInfo", {}).get("brand")),
            ("business type", advertiser.get("businessInfo", {}).get("businessType")),
            ("access policy groups", ", ".join(advertiser.get("accessPolicyGroups", []))),
            ("deduplication", advertiser.get("conversionTracking", {}).get("deduplication")),
            ("data centers", ", ".join(advertiser.get("technical", {}).get("traffic", {}).get("defaultSubcampaignDataCenters", []))),
            ("has_segment_new", "TRUE" if advertiser.get("technical", {}).get("visibilities", {}).get("hasSegmentNew") else "FALSE")
        ]
        
        for field_name, actual_value in fields:
            expected = expected_values.get(field_name)
            actual = actual_value or "N/A"
            
            if expected:
                if actual == expected:
                    status = " PASUJE"
                elif str(actual).startswith(expected[:5]):
                    status = " CZĘŚCIOWO PASUJE"
                else:
                    status = " NIE PASUJE"
            else:
                status = " BRAK OCZEKIWANEJ WARTOŚCI"
            
            self.health_results.insert(tk.END, f"{field_name:25}: {actual}\n")
            self.health_results.insert(tk.END, f"{'':25}  Status: {status}\n")
            if expected:
                self.health_results.insert(tk.END, f"{'':25}  Oczekiwane: {expected}\n")
            self.health_results.insert(tk.END, "\n")
    
    def save_campaign_config(self):
        if not self.health_check_passed:
            messagebox.showerror("Błąd", "Proszę najpierw wykonać health check")
            return
        
        campaign_id = self.campaign_id_var.get()
        if not campaign_id:
            messagebox.showerror("Błąd", "Wprowadź ID kampanii")
            return
        
        selected_fields = [field_id for field_id, var in self.field_vars.items() if var.get()]
        if not selected_fields:
            messagebox.showerror("Błąd", "Wybierz przynajmniej jedno pole")
            return
        
        # Collect field values
        config = {}
        row = 0
        for field_id, var in self.field_vars.items():
            if var.get():
                entry = self.field_config_frame.grid_slaves(row=row, column=1)[0]
                config[field_id] = entry.get()
                row += 1
        
        # Potwierdź przed wykonaniem mutacji
        result = messagebox.askyesno("Potwierdzenie", 
            f"Czy na pewno chcesz wykonać mutację GraphQL dla kampanii {campaign_id}?\n\n"
            f"Wybrane pola: {', '.join(selected_fields)}\n\n"
            f"To zmieni rzeczywiste dane w systemie!")
        
        if result:
            try:
                # Wykonaj prawdziwą mutację
                mutation_result = self.execute_campaign_mutation(int(campaign_id), config)
                messagebox.showinfo("Sukces", f"Mutacja GraphQL wykonana pomyślnie!\n\nWynik: {mutation_result}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas wykonywania mutacji: {str(e)}")
        else:
            messagebox.showinfo("Anulowano", "Mutacja została anulowana")
    
    def change_campaign_status(self):
        if not self.health_check_passed:
            messagebox.showerror("Błąd", "Najpierw wykonaj health check")
            return
        
        campaign_id = self.status_campaign_id_var.get()
        new_status = self.status_var.get()
        comment = self.comment_text.get(1.0, tk.END).strip()
        
        if not campaign_id or not new_status:
            messagebox.showerror("Błąd", "Wypełnij wszystkie wymagane pola")
            return
        
        # Potwierdź przed wykonaniem mutacji
        result = messagebox.askyesno("Potwierdzenie", 
            f"Czy na pewno chcesz wykonać mutację GraphQL?\n\n"
            f"Kampania: {campaign_id}\n"
            f"Nowy status: {new_status}\n"
            f"Komentarz: {comment}\n\n"
            f"To zmieni rzeczywisty status kampanii w systemie!")
        
        if result:
            try:
                # Wykonaj prawdziwą mutację statusu
                mutation_result = self.execute_status_mutation(int(campaign_id), new_status, comment)
                messagebox.showinfo("Sukces", f"Status kampanii zmieniony pomyślnie!\n\nWynik: {mutation_result}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas zmiany statusu: {str(e)}")
        else:
            messagebox.showinfo("Anulowano", "Zmiana statusu została anulowana")
    
    def execute_campaign_mutation(self, campaign_id, config):
        """Wykonuje prawdziwą mutację GraphQL dla kampanii"""
        
        mutations_executed = []
        
        # Automatyczne ustawienie obowiązkowych pól
        mandatory_config = {
            "dataCenters": ["ash", "phx", "sin", "ams"],
            "forceEnableGdprMacros": False,
            "subcampaignType": "performance-retargeting",
            "landingMacro": "https://www.rtbhouse.com/blog?utm_source=rtbhouse&utm_medium=performance&rtbhc={RTBHC}",
            "userSegments": ["BUYERS", "NEW", "SHOPPERS", "VISITORS"],
            "allowOneTagBids": True
        }
        
        # Połącz konfigurację użytkownika z obowiązkowymi polami
        full_config = {**mandatory_config, **config}
        
        # 0. Mutacja Data Centers (obowiązkowe)
        mutation = """
            mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                    properties {
                        dataCenters
                    }
                }
            }
        """
        
        input_data = {
            "dataCenters": mandatory_config["dataCenters"]
        }
        
        variables = {
            "subcampaignId": campaign_id,
            "input": input_data
        }
        
        response = self.make_graphql_request(mutation, variables)
        if response.get("data") and response["data"].get("updateSubcampaignInfo"):
            mutations_executed.append("Data Centers")
        
        # 1. Mutacja GDPR Macros (obowiązkowe)
        mutation = """
            mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                    properties {
                        forceEnableGdprMacros
                    }
                }
            }
        """
        
        input_data = {
            "forceEnableGdprMacros": mandatory_config["forceEnableGdprMacros"]
        }
        
        variables = {
            "subcampaignId": campaign_id,
            "input": input_data
        }
        
        response = self.make_graphql_request(mutation, variables)
        if response.get("data") and response["data"].get("updateSubcampaignInfo"):
            mutations_executed.append("GDPR Macros")
        
        # 2. Mutacja Subcampaign Type (obowiązkowe)
        mutation = """
            mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                    properties {
                        subcampaignType
                    }
                }
            }
        """
        
        input_data = {
            "subcampaignType": mandatory_config["subcampaignType"]
        }
        
        variables = {
            "subcampaignId": campaign_id,
            "input": input_data
        }
        
        response = self.make_graphql_request(mutation, variables)
        if response.get("data") and response["data"].get("updateSubcampaignInfo"):
            mutations_executed.append("Subcampaign Type")
        
        # 3. Mutacja Landing Macro (obowiązkowe)
        mutation = """
            mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                    landingMacro {
                        defaultUrl {
                            url
                        }
                    }
                }
            }
        """
        
        input_data = {
            "url": mandatory_config["landingMacro"]
        }
        
        variables = {
            "subcampaignId": campaign_id,
            "input": input_data
        }
        
        response = self.make_graphql_request(mutation, variables)
        if response.get("data") and response["data"].get("updateSubcampaignInfo"):
            mutations_executed.append("Landing Macro")
        
        # 4. Mutacja User Segments i Allow One Tag Bids (obowiązkowe)
        mutation = """
            mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                    targetingPolicy {
                        userPolicy {
                            allowOneTagBids
                            userSegments
                        }
                    }
                }
            }
        """
        
        input_data = {
            "userPolicy": {
                "allowOneTagBids": mandatory_config["allowOneTagBids"],
                "userSegments": mandatory_config["userSegments"]
            }
        }
        
        variables = {
            "subcampaignId": campaign_id,
            "input": input_data
        }
        
        response = self.make_graphql_request(mutation, variables)
        if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
            mutations_executed.append("User Segments & Allow One Tag Bids")
        
        # 5. Mutacja podstawowych informacji (nazwa, daty) - użytkownik
        if any(field in full_config for field in ["name", "startDate", "endDate"]):
            # Mutacja dla nazwy (oddzielna)
            if "name" in full_config:
                mutation = """
                    mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                        updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                            basicInfo { 
                                name 
                            }
                        }
                    }
                """
                
                input_data = {
                    "name": full_config["name"]
                }
                
                variables = {
                    "subcampaignId": campaign_id,
                    "input": input_data
                }
                
                response = self.make_graphql_request(mutation, variables)
                if response.get("data") and response["data"].get("updateSubcampaignInfo"):
                    mutations_executed.append("Nazwa kampanii")
                else:
                    raise Exception(f"Błąd mutacji nazwy: {response.get('errors', 'Nieznany błąd')}")
            
            # Mutacja dla dat (oddzielna)
            if any(field in full_config for field in ["startDate", "endDate"]):
                mutation = """
                    mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
                        updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
                            campaignStatus { 
                                startDate 
                                endDate 
                            }
                        }
                    }
                """
                
                input_data = {}
                if "startDate" in full_config:
                    input_data["startDate"] = full_config["startDate"]
                if "endDate" in full_config:
                    input_data["endDate"] = full_config["endDate"]
                
                variables = {
                    "subcampaignId": campaign_id,
                    "input": input_data
                }
                
                response = self.make_graphql_request(mutation, variables)
                if response.get("data") and response["data"].get("updateSubcampaignInfo"):
                    mutations_executed.append("Daty kampanii")
                else:
                    raise Exception(f"Błąd mutacji dat: {response.get('errors', 'Nieznany błąd')}")
        
        # 6. Mutacja limitów budżetowych - użytkownik
        if any(field in full_config for field in ["dailyBudget", "monthlyBudget"]):
            mutation = """
                mutation updateSubcampaignLimits($subcampaignId: Int!, $input: SubcampaignLimitsInput!) {
                    updateSubcampaignLimits(subcampaignId: $subcampaignId, input: $input) {
                        limits { 
                            budget { 
                                daily 
                                monthly 
                                comment
                            }
                        }
                    }
                }
            """
            
            input_data = {
                "budget": {
                    "comment": "Updated via Campaign Setup Automator"
                }
            }
            
            if "dailyBudget" in full_config:
                input_data["budget"]["daily"] = float(full_config["dailyBudget"])
            if "monthlyBudget" in full_config:
                input_data["budget"]["monthly"] = float(full_config["monthlyBudget"])
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignLimits"):
                mutations_executed.append("Limity budżetowe")
            else:
                raise Exception(f"Błąd mutacji limitów: {response.get('errors', 'Nieznany błąd')}")
        
        # 7. Mutacja limitów impresji - użytkownik
        if any(field in full_config for field in ["dailyImpressions", "monthlyImpressions"]):
            mutation = """
                mutation updateSubcampaignLimits($subcampaignId: Int!, $input: SubcampaignLimitsInput!) {
                    updateSubcampaignLimits(subcampaignId: $subcampaignId, input: $input) {
                        limits { 
                            events {
                                impressions {
                                    daily 
                                    monthly 
                                }
                            }
                        }
                    }
                }
            """
            
            input_data = {
                "events": {
                    "impressions": {}
                }
            }
            
            if "dailyImpressions" in full_config:
                input_data["events"]["impressions"]["daily"] = int(full_config["dailyImpressions"])
            if "monthlyImpressions" in full_config:
                input_data["events"]["impressions"]["monthly"] = int(full_config["monthlyImpressions"])
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignLimits"):
                mutations_executed.append("Limity impresji")
            else:
                raise Exception(f"Błąd mutacji limitów impresji: {response.get('errors', 'Nieznany błąd')}")
        
        # 8. Mutacja targeting policy (SSP) - użytkownik
        if any(field in full_config for field in ["allowedSSPs", "notAllowedSSPs"]):
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            sspPolicy {
                                allowedSsps
                                notAllowedSsps
                            }
                        }
                    }
                }
            """
            
            ssp_policy = {}
            
            if "allowedSSPs" in full_config:
                allowed_ssps = full_config["allowedSSPs"]
                if isinstance(allowed_ssps, str):
                    allowed_ssps = [ssp.strip() for ssp in allowed_ssps.split(",")]
                ssp_policy["allowedSsps"] = allowed_ssps
            
            if "notAllowedSSPs" in full_config:
                not_allowed_ssps = full_config["notAllowedSSPs"]
                if isinstance(not_allowed_ssps, str):
                    not_allowed_ssps = [ssp.strip() for ssp in not_allowed_ssps.split(",")]
                ssp_policy["notAllowedSsps"] = not_allowed_ssps
            
            input_data = {
                "sspPolicy": ssp_policy
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Targeting policy (SSP)")
            else:
                raise Exception(f"Błąd mutacji targeting: {response.get('errors', 'Nieznany błąd')}")
        
        # 9. Mutacja targeting policy (Deals) - użytkownik
        if any(field in full_config for field in ["allowedDeals", "notAllowedDeals"]):
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            dealPolicy {
                                allowedDeals
                                notAllowedDeals
                            }
                        }
                    }
                }
            """
            
            deal_policy = {}
            
            if "allowedDeals" in full_config:
                allowed_deals = full_config["allowedDeals"]
                if isinstance(allowed_deals, str):
                    allowed_deals = [deal.strip() for deal in allowed_deals.split(",")]
                deal_policy["allowedDeals"] = allowed_deals
            
            if "notAllowedDeals" in full_config:
                not_allowed_deals = full_config["notAllowedDeals"]
                if isinstance(not_allowed_deals, str):
                    not_allowed_deals = [deal.strip() for deal in not_allowed_deals.split(",")]
                deal_policy["notAllowedDeals"] = not_allowed_deals
            
            input_data = {
                "dealPolicy": deal_policy
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Targeting policy (Deals)")
            else:
                raise Exception(f"Błąd mutacji targeting deals: {response.get('errors', 'Nieznany błąd')}")
        
        # 10. Mutacja Ad API Framework - użytkownik
        if "supportedAdApiFrameworks" in full_config:
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            adApiFrameworkPolicy {
                                supportedAdApiFrameworks
                            }
                        }
                    }
                }
            """
            
            frameworks = full_config["supportedAdApiFrameworks"]
            if isinstance(frameworks, str):
                frameworks = [fw.strip() for fw in frameworks.split(",")]
            
            input_data = {
                "adApiFrameworkPolicy": {
                    "supportedAdApiFrameworks": frameworks
                }
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Ad API Framework")
            else:
                raise Exception(f"Błąd mutacji Ad API Framework: {response.get('errors', 'Nieznany błąd')}")
        
        # 11. Mutacja Profile Identifiers - użytkownik
        if any(field in full_config for field in ["allowedProfileIdentifierTypes", "notAllowedProfileIdentifierTypes"]):
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            userPolicy {
                                profileIdentifiers {
                                    allowedProfileIdentifierTypes
                                    notAllowedProfileIdentifierTypes
                                }
                            }
                        }
                    }
                }
            """
            
            profile_policy = {}
            
            if "allowedProfileIdentifierTypes" in full_config:
                allowed_types = full_config["allowedProfileIdentifierTypes"]
                if isinstance(allowed_types, str):
                    allowed_types = [t.strip() for t in allowed_types.split(",")]
                profile_policy["allowedProfileIdentifierTypes"] = allowed_types
            
            if "notAllowedProfileIdentifierTypes" in full_config:
                not_allowed_types = full_config["notAllowedProfileIdentifierTypes"]
                if isinstance(not_allowed_types, str):
                    not_allowed_types = [t.strip() for t in not_allowed_types.split(",")]
                profile_policy["notAllowedProfileIdentifierTypes"] = not_allowed_types
            
            input_data = {
                "userPolicy": {
                    "profileIdentifiers": profile_policy
                }
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Profile Identifiers")
            else:
                raise Exception(f"Błąd mutacji Profile Identifiers: {response.get('errors', 'Nieznany błąd')}")
        
        # 12. Mutacja Mobile Placement - użytkownik
        if "fullscreenMobilePlacement" in full_config:
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            inAppsPolicy {
                                fullscreenMobilePlacement
                            }
                        }
                    }
                }
            """
            
            input_data = {
                "inAppsPolicy": {
                    "fullscreenMobilePlacement": full_config["fullscreenMobilePlacement"]
                }
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Mobile Placement")
            else:
                raise Exception(f"Błąd mutacji Mobile Placement: {response.get('errors', 'Nieznany błąd')}")
        
        # 13. Mutacja Bidding Model CPM - użytkownik
        if any(field in full_config for field in ["cpmVisitors", "cpmShoppers", "cpmBuyers", "cpmNew"]):
            mutation = """
                mutation UpdateSubcampaignBiddingModel($subcampaignId: Int!, $input: BiddingModelInput!) {
                    updateSubcampaignBiddingModel(subcampaignId: $subcampaignId, input: $input) {
                        biddingModel {
                            cpm {
                                buyers
                                new
                                shoppers
                                visitors
                            }
                        }
                    }
                }
            """
            
            cpm_data = {}
            
            if "cpmVisitors" in full_config:
                cpm_data["visitors"] = float(full_config["cpmVisitors"])
            if "cpmShoppers" in full_config:
                cpm_data["shoppers"] = float(full_config["cpmShoppers"])
            if "cpmBuyers" in full_config:
                cpm_data["buyers"] = float(full_config["cpmBuyers"])
            if "cpmNew" in full_config:
                cpm_data["new"] = float(full_config["cpmNew"])
            
            input_data = {
                "cpm": cpm_data
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignBiddingModel"):
                mutations_executed.append("Bidding model CPM")
            else:
                raise Exception(f"Błąd mutacji Bidding Model: {response.get('errors', 'Nieznany błąd')}")
        
        # 14. Mutacja Device Types - użytkownik
        if any(field in full_config for field in ["allowedDeviceTypes", "notAllowedDeviceTypes"]):
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            deviceTypePolicy {
                                allowedDeviceTypes
                                notAllowedDeviceTypes
                            }
                        }
                    }
                }
            """
            
            device_policy = {}
            
            if "allowedDeviceTypes" in full_config:
                allowed_types = full_config["allowedDeviceTypes"]
                if isinstance(allowed_types, str):
                    allowed_types = [t.strip() for t in allowed_types.split(",")]
                device_policy["allowedDeviceTypes"] = allowed_types
            
            if "notAllowedDeviceTypes" in full_config:
                not_allowed_types = full_config["notAllowedDeviceTypes"]
                if isinstance(not_allowed_types, str):
                    not_allowed_types = [t.strip() for t in not_allowed_types.split(",")]
                device_policy["notAllowedDeviceTypes"] = not_allowed_types
            
            input_data = {
                "deviceTypePolicy": device_policy
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Device Types")
            else:
                raise Exception(f"Błąd mutacji Device Types: {response.get('errors', 'Nieznany błąd')}")
        
        # 15. Mutacja geotargetingu - użytkownik
        if any(field in full_config for field in ["includedCountriesCountry", "excludedCountries", "includedRegions", "includedCitiesCity"]):
            mutation = """
                mutation ($subcampaignId: Int!, $input: GeotargetingInput!) {
                    updateSubcampaignGeotargeting(subcampaignId: $subcampaignId, input: $input) {
                        subcampaignId
                        geotargeting {
                            includedCountries {
                                country
                                includedRegions
                                excludedRegions
                                includedCities {
                                    region
                                    city
                                }
                            }
                            excludedCountries
                        }
                    }
                }
            """
            
            input_data = {}
            
            if "excludedCountries" in full_config:
                excluded_countries = full_config["excludedCountries"]
                if isinstance(excluded_countries, str):
                    excluded_countries = [country.strip() for country in excluded_countries.split(",")]
                input_data["excludedCountries"] = excluded_countries
            
            if "includedCountriesCountry" in full_config:
                included_countries = full_config["includedCountriesCountry"]
                if isinstance(included_countries, str):
                    included_countries = [country.strip() for country in included_countries.split(",")]
                
                included_countries_data = []
                for country in included_countries:
                    country_data = {"country": country}
                    
                    if "includedRegions" in full_config:
                        regions = full_config["includedRegions"]
                        if isinstance(regions, str):
                            regions = [region.strip() for region in regions.split(",")]
                        country_data["includedRegions"] = regions
                    
                    if "includedCitiesCity" in full_config:
                        cities = full_config["includedCitiesCity"]
                        if isinstance(cities, str):
                            cities = [city.strip() for city in cities.split(",")]
                        country_data["includedCities"] = [{"region": "", "city": city} for city in cities]
                    
                    included_countries_data.append(country_data)
                
                input_data["includedCountries"] = included_countries_data
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignGeotargeting"):
                mutations_executed.append("Geotargeting")
            else:
                raise Exception(f"Błąd mutacji geotargetingu: {response.get('errors', 'Nieznany błąd')}")
        
        # 16. Mutacja Creative IDs - użytkownik
        if "creativeIds" in full_config:
            mutation = """
                mutation UpdateSubcampaignCreatives($subcampaignId: Int!, $input: SubcampaignCreativesInput!) {
                    updateSubcampaignCreatives(subcampaignId: $subcampaignId, input: $input) {
                        creatives {
                            creativeId
                        }
                    }
                }
            """
            
            creative_ids = full_config["creativeIds"]
            if isinstance(creative_ids, str):
                creative_ids = [id.strip() for id in creative_ids.split(",")]
            
            input_data = {
                "creatives": [{"creativeId": id} for id in creative_ids]
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignCreatives"):
                mutations_executed.append("Creative IDs")
            else:
                raise Exception(f"Błąd mutacji Creative IDs: {response.get('errors', 'Nieznany błąd')}")
        
        # 17. Mutacja Placement Environment - użytkownik
        if any(field in full_config for field in ["allowedPlacementEnvironments", "notAllowedPlacementEnvironments"]):
            mutation = """
                mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
                    updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
                        targetingPolicy {
                            placementEnvironmentPolicy {
                                allowedPlacementEnvironments
                                notAllowedPlacementEnvironments
                            }
                        }
                    }
                }
            """
            
            placement_policy = {}
            
            if "allowedPlacementEnvironments" in full_config:
                allowed_envs = full_config["allowedPlacementEnvironments"]
                if isinstance(allowed_envs, str):
                    allowed_envs = [env.strip() for env in allowed_envs.split(",")]
                placement_policy["allowedPlacementEnvironments"] = allowed_envs
            
            if "notAllowedPlacementEnvironments" in full_config:
                not_allowed_envs = full_config["notAllowedPlacementEnvironments"]
                if isinstance(not_allowed_envs, str):
                    not_allowed_envs = [env.strip() for env in not_allowed_envs.split(",")]
                placement_policy["notAllowedPlacementEnvironments"] = not_allowed_envs
            
            input_data = {
                "placementEnvironmentPolicy": placement_policy
            }
            
            variables = {
                "subcampaignId": campaign_id,
                "input": input_data
            }
            
            response = self.make_graphql_request(mutation, variables)
            if response.get("data") and response["data"].get("updateSubcampaignTargetingPolicy"):
                mutations_executed.append("Placement Environment")
            else:
                raise Exception(f"Błąd mutacji Placement Environment: {response.get('errors', 'Nieznany błąd')}")
        
        return f"Wykonano mutacje: {', '.join(mutations_executed)}"
    
    def execute_status_mutation(self, campaign_id, new_status, comment):
        """Wykonuje prawdziwą mutację GraphQL dla statusu kampanii"""
        mutation = """
            mutation UpdateSubcampaignCampaignStatus($subcampaignId: Int!, $input: UpdateSubcampaignCampaignStatusInput!) {
                updateSubcampaignCampaignStatus(subcampaignId: $subcampaignId, input: $input) {
                    campaignStatus {
                        status {
                            value
                        }
                    }
                }
            }
        """
        
        # Poprawna struktura zgodnie z update_kampanii.md
        variables = {
            "subcampaignId": campaign_id,
            "input": {
                "status": {
                    "value": new_status  # Status musi być w obiekcie z polem "value"
                }
            }
        }
        
        response = self.make_graphql_request(mutation, variables)
        
        if response.get("data") and response["data"].get("updateSubcampaignCampaignStatus"):
            return response["data"]["updateSubcampaignCampaignStatus"]
        else:
            raise Exception(f"Błąd mutacji: {response.get('errors', 'Nieznany błąd')}")
    
    def make_graphql_request(self, query, variables=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{self.auth['username']}:{self.auth['password']}'.encode()).decode()}"
        }
        
        data = {"query": query}
        if variables:
            data["variables"] = variables
        
        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        # Disable SSL verification for development
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            return json.loads(response.read().decode("utf-8"))

def main():
    root = tk.Tk()
    app = CampaignSetupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()