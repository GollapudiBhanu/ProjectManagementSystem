import os
import pandas as pd
import numpy as np

class Completeness:

    def __init__(self):
        self.features = ["API", "Access Controls Permissions",
                    "Accounting Integration",
                    "Activity Dashboard",
                    "Activity Management",
                    "Activity Tracking",
                    "Alerts Notifications",
                    "Appointment Scheduling",
                    "Billing & Invoicing",
                    "Calendar Management",
                    "Calendar Sync",
                    "Campaign Analytics",
                    "Campaign Management",
                    "Cataloging Categorization",
                    "Chat Messaging",
                    "Client Management",
                    "Client Portal",
                    "Collaboration Tools",
                    "Commission Management",
                    "Communication Management",
                    "Configurable Workflow",
                    "Contact Database",
                    "Contact Management",
                    "Content Management",
                    "Contract License Management",
                    "CRM",
                    "Customer Database",
                    "Customer History",
                    "Customer Segmentation",
                    "Customer Service Analytics",
                    "Customizable Branding",
                    "Customizable Fields",
                    "Customizable Forms",
                    "Customizable Reports",
                    "Customizable Templates",
                    "Data Import Export",
                    "Data Visualization",
                    "Document Management",
                    "Document Storage",
                    "Drag  Drop",
                    "Drip Campaigns",
                    "Email Management",
                    "Email Marketing",
                    "Email Templates",
                    "Email Tracking",
                    "Engagement Tracking",
                    "Event Triggered Actions",
                    "Financial Management",
                    "Forecasting",
                    "Interaction Tracking",
                    "Inventory Management",
                    "Invoice Management",
                    "Landing Pages Web Forms",
                    "Lead Capture",
                    "Lead Distribution",
                    "Lead Generation",
                    "Lead Management",
                    "Lead Nurturing",
                    "Lead Qualification",
                    "Live Chat",
                    "Mobile Access",
                    "Monitoring",
                    "Multi-Channel Communication",
                    "Multi-Channel Marketing",
                    "Multi-Currency",
                    "Opportunity Management",
                    "Order Management",
                    "Performance Metrics",
                    "Pipeline Management",
                    "Pipeline Reports",
                    "Prioritization",
                    "Project Management",
                    "Projections",
                    "Proposal Generation",
                    "Purchase Order Management",
                    "Quotes/Estimates",
                    "Real Time Analytics",
                    "Real Time Data",
                    "Real Time Notifications",
                    "Real Time Reporting",
                    "Real-time Updates",
                    "Referral Tracking",
                    "Reminders",
                    "Reporting & Statistics",
                    "Reporting/Analytics",
                    "Role-Based Permissions",
                    "Sales Forecasting",
                    "Sales Reports",
                    "Scheduling",
                    "Search/Filter",
                    "Self Service Portal",
                    "Social Media Integration",
                    "Third Party Integrations",
                    "Task Management",
                    "Task Scheduling",
                    "Template Management",
                    "Territory Management",
                    "Time & Expense Tracking",
                    "Web Forms",
                    "Workflow Management"]

    def completeness(self, dir_path, out_dirptah):
        csv_files = os.listdir(dir_path)
        for csvfile in csv_files:
            if csvfile == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + csvfile)

            df['reviewDescription'].replace(np.nan, '', inplace=True)
            df['pros'].replace(np.nan, '', inplace=True)
            df['cons'].replace(np.nan, '', inplace=True)

            descriptionList = df['reviewDescription'].values.tolist()
            prosList = df['pros'].values.tolist()
            consList = df['cons'].values.tolist()

            descriptionRel = self.calculateDescriptionrelevance(descriptionList)
            prosRel = self.calculateProrelevance(prosList)
            consList = self.calculateConsrelevance(consList)

            df['Description_Completeness'] = descriptionRel
            df['Pros_Completeness'] = prosRel
            df['Cons_Completeness'] = consList

            df.to_csv(out_dirptah + csvfile, index=None)


    def calculateDescriptionrelevance(self, descriptionList):
        description_rel_list = []
        for description in descriptionList:
            relDict = self.calculateFeatureRelevance(description)
            description_rel_list.append(relDict)
        return description_rel_list

    def calculateProrelevance(self, prosList):
        pros_list = []
        for pros in prosList:
            relDict = self.calculateFeatureRelevance(pros)
            pros_list.append(relDict)
        return pros_list

    def calculateConsrelevance(self, consList):
        cons_rel_list = []
        for cons in consList:
            relDict = self.calculateFeatureRelevance(cons)
            cons_rel_list.append(relDict)
        return cons_rel_list

    def calculateFeatureRelevance(self, text):
        countDict = {}
        for feature in self.features:
            countDict[feature] = text.lower().count(feature.lower())
        return countDict


if __name__ == '__main__':
    obj = Completeness()
    obj.completeness('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Sentimetal analysis/',
                     '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GetApp_Completeness/')



