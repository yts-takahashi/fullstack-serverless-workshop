import React from 'react';
import './App.css';

import { Authenticator, withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

// Appコンポーネントの定義 (内容はひとまずそのままでOK)
function App() {
  return (
    // Authenticatorでアプリ全体を囲む
    <Authenticator loginMechanisms={['email']}>
      {({ signOut, user }) => (
        <main>
          <h1>Hello {user.username}</h1>
          <p>Todoリストのコンテンツはここに表示します。</p>
          <button onClick={signOut}>Sign out</button>
        </main>
      )}
    </Authenticator>
  );
}

export default withAuthenticator(App);