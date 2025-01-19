const { contextBridge } = require("electron");
const Store = require("electron-store");

const store = new Store();

contextBridge.exposeInMainWorld("store", {
  set: (key, value) => store.set(key, value),
  get: (key) => store.get(key),
  delete: (key) => store.delete(key),
});

const { activeWindow } = require("get-windows");

contextBridge.exposeInMainWorld("windowAPI", {
  getActiveWindow: async () => {
    const result = await activeWindow();
    return result;
  },
});
