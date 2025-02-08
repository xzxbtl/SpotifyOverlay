using System.Diagnostics;
using System.Runtime.InteropServices;
using GlobalHotKeys;
using GlobalHotKeys.Native.Types;
using static System.Runtime.CompilerServices.RuntimeHelpers;

namespace Spotify{
    public class Spotify
    {
        [DllImport("user32.dll")]
        static extern bool SetForegroundWindow(IntPtr hWnd);

        private static string nameProcess = "Spotify";

        private const int SW_RESTORE = 9;
        private const int SW_HIDE = 0;
        private const int KEYEVENTF_KEYUP = 0x0002;


        private static string activeProcess = "";
        private static bool isHotKeyPressed = false;

        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        public static extern UInt32 GetWindowThreadProcessId(IntPtr hwnd, ref Int32 pid);

        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [DllImport("user32.dll")]
        static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);

        public enum KeyCode : byte
        {
            VK_CONTROL = 0x11, // Ctrl
            VK_RIGHT = 0x27,    // Стрелка вправо
            VK_LEFT = 0x25,
            VK_SPACE = 0x20,
            VK_UP = 0x26,
            VK_DOWN = 0x28
        }

        private static void Main(string[] args)
        {
            Process[] processingApps = Process.GetProcesses();
            ContollKeyboardPerssed();
            Console.ReadLine();

        }

        // Активирует и разворачивает приложение
        private static void ActivateApp(Process[] listProcesses, string processName)
        {
            Process[] app = Process.GetProcessesByName(processName);
            if (app.Length > 0)
            {
                IntPtr hWnd = app[0].MainWindowHandle;
                if (hWnd != IntPtr.Zero)
                {
                    ShowWindow(hWnd, SW_RESTORE);
                    SetForegroundWindow(hWnd);
                    Console.Write(app);
                    Thread.Sleep(100);
                }
            }
        }

        // Скрывает приложение
        private static void HideApp(Process[] listProcesses,string processName)
        {
            Process[] app = Process.GetProcessesByName(processName);
            if (app.Length > 0)
            {
                IntPtr hWnd = app[0].MainWindowHandle;
                if (hWnd != IntPtr.Zero)
                {
                    ShowWindow(hWnd, SW_HIDE);
                    Thread.Sleep(100);
                }
            }
        }

        // Получает последнее активное приложение и заносит название процесса в переменную
        private static void GetActiveWindow()
        {
            IntPtr active = GetForegroundWindow();
            int pid = 0;
            GetWindowThreadProcessId(active, ref pid);
            Process app = Process.GetProcessById(pid);
            activeProcess = app.ProcessName;

            Console.Write(activeProcess);
        }

        // Отслеживает Нажатия на кнопки
        private static void ContollKeyboardPerssed()
        {
            var hotKeyManager = new HotKeyManager();
            var subscription = hotKeyManager.HotKeyPressed.Subscribe(HotKeyPressed);
            
            var altspaceKey = hotKeyManager.Register(VirtualKeyCode.VK_SPACE, Modifiers.Shift);
            var altRightArrow = hotKeyManager.Register(VirtualKeyCode.VK_RIGHT, Modifiers.Shift);
            var altLeftArrow = hotKeyManager.Register(VirtualKeyCode.VK_LEFT, Modifiers.Shift);
            var altUpArrow = hotKeyManager.Register(VirtualKeyCode.VK_UP, Modifiers.Shift);
            var altDownArrow = hotKeyManager.Register(VirtualKeyCode.VK_DOWN, Modifiers.Shift);
        }

        private static void HotKeyPressed(HotKey hotKey)
        {
            if (isHotKeyPressed) return;
            isHotKeyPressed = true;
            try
            {
                if (hotKey.Key == VirtualKeyCode.VK_RIGHT)
                {
                    ActivateAllActions((byte)KeyCode.VK_CONTROL, (byte)KeyCode.VK_RIGHT);
                }
                if (hotKey.Key == VirtualKeyCode.VK_LEFT)
                {
                    ActivateAllActions((byte)KeyCode.VK_CONTROL, (byte)KeyCode.VK_LEFT);
                }
                if (hotKey.Key == VirtualKeyCode.VK_SPACE)
                {
                    ActivateSpaceActions((byte)KeyCode.VK_SPACE);
                }
                if (hotKey.Key == VirtualKeyCode.VK_UP)
                {
                    ActivateAllActions((byte)KeyCode.VK_CONTROL, (byte)KeyCode.VK_UP);
                }
                if (hotKey.Key == VirtualKeyCode.VK_DOWN)
                {
                    ActivateAllActions((byte)KeyCode.VK_CONTROL, (byte)KeyCode.VK_DOWN);
                }
            }
            finally
            {
                // Сброс флага через определенное время или по какому-то событию
                Task.Delay(200).ContinueWith(t => isHotKeyPressed = false);
            }
        }

        static void SimulateKeyPress(byte key1, byte key2)
        {
            keybd_event(key1, 0, 0, UIntPtr.Zero);
            keybd_event(key2, 0, 0, UIntPtr.Zero);

            keybd_event(key2, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
            keybd_event(key1, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        }
        static void SimulateSpacePress(byte key)
        {
            keybd_event(key, 0, 0, UIntPtr.Zero);
            keybd_event(key, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        }


        static void ActivateAllActions(byte key1, byte key2)
        {
            Process[] processingApps = Process.GetProcesses();
            
            GetActiveWindow();

            ActivateApp(processingApps, nameProcess);
            Thread.Sleep(100);

            SimulateKeyPress(key1, key2);
            Thread.Sleep(100);

            Thread.Sleep(100);

            ActivateApp(processingApps, activeProcess);
        }

        static void ActivateSpaceActions(byte key1)
        {
            Process[] processingApps = Process.GetProcesses();

            GetActiveWindow();

            ActivateApp(processingApps, nameProcess);
            Thread.Sleep(100);

            SimulateSpacePress((byte)KeyCode.VK_SPACE);
            Thread.Sleep(100);

            Thread.Sleep(100);

            ActivateApp(processingApps, activeProcess);
        }
    }
}


