import { combineReducers } from 'redux';
import { configureStore, getDefaultMiddleware } from '@reduxjs/toolkit';
import { userSlice } from './../redux/UserSlice';
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore } from 'redux-persist';

const persistConfig = {
    key: 'root',
    storage,
    // Add this line to ignore non-serializable values
    serialize: false,
};

// Add new reducers the same way.
const rootReducer = combineReducers({
    userReducer: userSlice.reducer
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
    reducer: persistedReducer,
    middleware: getDefaultMiddleware({
        serializableCheck: {
            // Ignore these action types
            ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
            // Ignore these paths in the state
            ignoredPaths: ['register'],
        },
    }),
});

const persistor = persistStore(store);

export { store, persistor };