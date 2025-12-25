import streamlit as st
import json
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide", page_title="The NCERT Knowledge Graph")

# 1. THE DATA (Paste your ChatGPT JSON here)
raw_json = '''
[
  [
  { "source": "Force", "target": "Motion & Force", "relation": "is_part_of", "grade": "7" },
  { "source": "Motion", "target": "Motion & Force", "relation": "is_part_of", "grade": "7" },
  { "source": "Speed", "target": "Motion & Force", "relation": "connects_to", "grade": "7" },
  { "source": "Acceleration", "target": "Motion & Force", "relation": "connects_to", "grade": "8" },
  { "source": "Friction", "target": "Motion & Force", "relation": "is_part_of", "grade": "8" },
  { "source": "Gravity", "target": "Motion & Force", "relation": "is_part_of", "grade": "8" },

  { "source": "Light", "target": "Light & Sound", "relation": "is_part_of", "grade": "7" },
  { "source": "Reflection", "target": "Light & Sound", "relation": "connects_to", "grade": "7" },
  { "source": "Refraction", "target": "Light & Sound", "relation": "connects_to", "grade": "8" },
  { "source": "Dispersion of Light", "target": "Light & Sound", "relation": "is_part_of", "grade": "8" },
  { "source": "Sound", "target": "Light & Sound", "relation": "is_part_of", "grade": "7" },
  { "source": "Vibration", "target": "Light & Sound", "relation": "connects_to", "grade": "7" },

  { "source": "Electric Current", "target": "Electricity & Magnetism", "relation": "is_part_of", "grade": "7" },
  { "source": "Electric Circuit", "target": "Electricity & Magnetism", "relation": "is_part_of", "grade": "7" },
  { "source": "Electric Cell", "target": "Electricity & Magnetism", "relation": "connects_to", "grade": "7" },
  { "source": "Magnet", "target": "Electricity & Magnetism", "relation": "is_part_of", "grade": "7" },
  { "source": "Magnetic Poles", "target": "Electricity & Magnetism", "relation": "connects_to", "grade": "7" },
  { "source": "Electromagnet", "target": "Electricity & Magnetism", "relation": "is_part_of", "grade": "8" },

  { "source": "Heat", "target": "Heat", "relation": "is_part_of", "grade": "7" },
  { "source": "Temperature", "target": "Heat", "relation": "connects_to", "grade": "7" },
  { "source": "Conduction", "target": "Heat", "relation": "is_part_of", "grade": "7" },
  { "source": "Convection", "target": "Heat", "relation": "is_part_of", "grade": "8" },
  { "source": "Radiation", "target": "Heat", "relation": "is_part_of", "grade": "8" },

  { "source": "Matter", "target": "Matter & Materials", "relation": "is_part_of", "grade": "7" },
  { "source": "Physical Properties", "target": "Matter & Materials", "relation": "connects_to", "grade": "7" },
  { "source": "States of Matter", "target": "Matter & Materials", "relation": "is_part_of", "grade": "7" },
  { "source": "Elements", "target": "Matter & Materials", "relation": "is_part_of", "grade": "8" },
  { "source": "Compounds", "target": "Matter & Materials", "relation": "connects_to", "grade": "8" },
  { "source": "Mixtures", "target": "Matter & Materials", "relation": "connects_to", "grade": "7" },

  { "source": "Chemical Reaction", "target": "Chemical Changes", "relation": "is_part_of", "grade": "7" },
  { "source": "Rusting", "target": "Chemical Changes", "relation": "connects_to", "grade": "7" },
  { "source": "Burning", "target": "Chemical Changes", "relation": "connects_to", "grade": "7" },
  { "source": "Oxidation", "target": "Chemical Changes", "relation": "is_part_of", "grade": "8" },
  { "source": "Reduction", "target": "Chemical Changes", "relation": "connects_to", "grade": "8" },

  { "source": "Acids", "target": "Acids, Bases & Salts", "relation": "is_part_of", "grade": "7" },
  { "source": "Bases", "target": "Acids, Bases & Salts", "relation": "is_part_of", "grade": "7" },
  { "source": "Salts", "target": "Acids, Bases & Salts", "relation": "is_part_of", "grade": "7" },
  { "source": "Indicators", "target": "Acids, Bases & Salts", "relation": "connects_to", "grade": "7" },
  { "source": "Neutralisation", "target": "Acids, Bases & Salts", "relation": "connects_to", "grade": "7" },

  { "source": "Living Organisms", "target": "Living Organisms", "relation": "is_part_of", "grade": "7" },
  { "source": "Cell", "target": "Living Organisms", "relation": "connects_to", "grade": "8" },
  { "source": "Tissue", "target": "Living Organisms", "relation": "connects_to", "grade": "8" },
  { "source": "Microorganisms", "target": "Living Organisms", "relation": "is_part_of", "grade": "8" },

  { "source": "Nutrition", "target": "Food & Nutrition", "relation": "is_part_of", "grade": "7" },
  { "source": "Carbohydrates", "target": "Food & Nutrition", "relation": "connects_to", "grade": "7" },
  { "source": "Proteins", "target": "Food & Nutrition", "relation": "connects_to", "grade": "7" },
  { "source": "Fats", "target": "Food & Nutrition", "relation": "connects_to", "grade": "7" },
  { "source": "Vitamins", "target": "Food & Nutrition", "relation": "connects_to", "grade": "7" },

  { "source": "Digestive System", "target": "Human Body", "relation": "is_part_of", "grade": "7" },
  { "source": "Respiratory System", "target": "Human Body", "relation": "is_part_of", "grade": "7" },
  { "source": "Circulatory System", "target": "Human Body", "relation": "is_part_of", "grade": "8" },
  { "source": "Excretory System", "target": "Human Body", "relation": "is_part_of", "grade": "8" },

  { "source": "Plants", "target": "Plants", "relation": "is_part_of", "grade": "7" },
  { "source": "Photosynthesis", "target": "Plants", "relation": "connects_to", "grade": "7" },
  { "source": "Transpiration", "target": "Plants", "relation": "connects_to", "grade": "7" },
  { "source": "Reproduction in Plants", "target": "Plants", "relation": "is_part_of", "grade": "8" },

  { "source": "Ecosystem", "target": "Ecosystem", "relation": "is_part_of", "grade": "8" },
  { "source": "Food Chain", "target": "Ecosystem", "relation": "connects_to", "grade": "8" },
  { "source": "Food Web", "target": "Ecosystem", "relation": "connects_to", "grade": "8" },
  { "source": "Producers", "target": "Ecosystem", "relation": "connects_to", "grade": "8" },
  { "source": "Consumers", "target": "Ecosystem", "relation": "connects_to", "grade": "8" },
  { "source": "Decomposers", "target": "Ecosystem", "relation": "connects_to", "grade": "8" }
]

]
'''
data = json.loads(raw_json)

# 2. THE LOGIC
nodes = []
edges = []
nodes_added = set()

# Color Coding
grade_colors = {"6": "#FFD700", "7": "#FF8C00", "8": "#FF4500"}
hub_color = "#1E90FF" 

# We loop through the list 'data'
for item in data:
    # We ensure 'item' is a dictionary before calling .get()
    if isinstance(item, dict):
        source_node = item.get("source")
        target_node = item.get("target")
        grade = str(item.get("grade", "7")) # Convert to string just in case
        rel = item.get("relation", "is_part_of")

        # Add Source Node (The Concept)
        if source_node and source_node not in nodes_added:
            nodes.append(Node(id=source_node, 
                              label=source_node, 
                              size=15, 
                              color=grade_colors.get(grade, "#6495ED")))
            nodes_added.add(source_node)
        
        # Add Target Node (The Hub)
        if target_node and target_node not in nodes_added:
            nodes.append(Node(id=target_node, 
                              label=target_node, 
                              size=35, 
                              color=hub_color, 
                              shape="diamond"))
            nodes_added.add(target_node)
            
        # Create the connection
        if source_node and target_node:
            edges.append(Edge(source=source_node, target=target_node, label=rel))
# 3. THE UI
st.title("🌌 The NCERT Knowledge Graph")
st.write("A Galaxy View of Science: Explore how Class 7 and 8 concepts orbit central scientific themes.")

config = Config(width=1000, 
                height=800, 
                directed=True, 
                physics=True, 
                hierarchical=False,
                collapsible=True # This lets you "shrink" hubs by clicking them
                )

# This line renders the graph
agraph(nodes=nodes, edges=edges, config=config)
