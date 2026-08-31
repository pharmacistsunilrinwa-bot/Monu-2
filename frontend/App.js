import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';

const MonuApp = () => {
  const [message, setMessage] = useState('');

  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>MONU AI</Text>
        <Text style={styles.status}>Internet ● Server ●</Text>
      </View>
      <ScrollView style={styles.chatArea}>
        {/* Placeholder for Chat Messages */}
        <Text>Welcome to MONU AI Master Workspace</Text>
      </ScrollView>
      <View style={styles.chatbox}>
        <TouchableOpacity style={styles.button}><Text>+</Text></TouchableOpacity>
        <TouchableOpacity style={styles.button}><Text>🎤</Text></TouchableOpacity>
        <TextInput style={styles.input} value={message} onChangeText={setMessage} placeholder="Type message..." />
        <TouchableOpacity style={styles.button}><Text>➤</Text></TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { padding: 20, backgroundColor: '#fff', borderBottomWidth: 1, borderColor: '#eee' },
  title: { fontSize: 20, fontWeight: 'bold' },
  status: { color: 'green' },
  chatArea: { flex: 1, padding: 20 },
  chatbox: { flexDirection: 'row', padding: 10, backgroundColor: '#fff', borderTopWidth: 1, borderColor: '#eee' },
  input: { flex: 1, marginHorizontal: 10, padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 20 },
  button: { padding: 10 }
});

export default MonuApp;
