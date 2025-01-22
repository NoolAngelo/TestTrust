from graphviz import Digraph

dot = Digraph(comment='Flowchart')

# System Initialization
dot.node('A', 'Start')
dot.node('B', 'Load Chrome Extension')
dot.node('C', 'Check Login Status')
dot.edges(['AB', 'BC'])

# Authentication Process
dot.node('D', 'Show Login Form')
dot.node('E', 'Validate Credentials')
dot.node('F', 'Store Auth Token')
dot.node('G', 'Show Main Interface')
dot.edge('C', 'D', label='Not Logged In')
dot.edge('D', 'E')
dot.edge('E', 'D', label='Invalid')
dot.edge('E', 'F', label='Valid')
dot.edge('F', 'G')

# Exam Setup
dot.node('H', 'Initialize Exam Controls')
dot.node('I', 'Check System Requirements')
dot.node('J', 'Requirements Met?')
dot.node('K', 'Show System Requirements Error')
dot.node('L', 'Ready for Exam')
dot.edge('G', 'H')
dot.edge('H', 'I')
dot.edge('I', 'J')
dot.edge('J', 'K', label='No')
dot.edge('K', 'H')
dot.edge('J', 'L', label='Yes')

# Monitoring System
dot.node('M', 'Start Monitoring Services')
dot.node('N', 'Initialize Camera')
dot.node('O', 'Start Iris Detection')
dot.node('P', 'Start Behavior Monitoring')
dot.edge('L', 'M')
dot.edge('M', 'N')
dot.edge('N', 'O')
dot.edge('O', 'P')

# Real-time Security Checks
dot.node('Q', 'Monitor Eye Movement')
dot.node('R', 'Track Face Position')
dot.node('S', 'Check For Multiple Faces')
dot.node('T', 'Monitor Tab Switching')
dot.node('U', 'Check Screen Recording')
dot.edge('P', 'Q')
dot.edge('Q', 'R')
dot.edge('R', 'S')
dot.edge('S', 'T')
dot.edge('T', 'U')
dot.edge('U', 'Q')

# Violation Detection & Handling
dot.node('V', 'Detect Violation?')
dot.node('W', 'Log Violation')
dot.node('X', 'Send Alert to Proctor')
dot.node('Y', 'Serious Violation?')
dot.node('Z', 'Pause Exam')
dot.node('AA', 'Wait for Proctor Review')
dot.edge('Q', 'V')
dot.edge('V', 'W', label='Yes')
dot.edge('W', 'X')
dot.edge('X', 'Y')
dot.edge('Y', 'Q', label='No')
dot.edge('Y', 'Z', label='Yes')
dot.edge('Z', 'AA')
dot.edge('AA', 'Q')

# Exam Completion
dot.node('BB', 'Exam Finished?')
dot.node('CC', 'Stop Monitoring')
dot.node('DD', 'Generate Security Report')
dot.node('EE', 'Save Session Data')
dot.node('FF', 'End Exam Mode')
dot.edge('V', 'BB', label='No')
dot.edge('BB', 'Q', label='No')
dot.edge('BB', 'CC', label='Yes')
dot.edge('CC', 'DD')
dot.edge('DD', 'EE')
dot.edge('EE', 'FF')

# System Cleanup
dot.node('GG', 'Release Camera')
dot.node('HH', 'Clear Temporary Data')
dot.node('II', 'Return to Main Interface')
dot.edge('FF', 'GG')
dot.edge('GG', 'HH')
dot.edge('HH', 'II')

# Save and render the graph
dot.render('flowchart.gv', view=True)