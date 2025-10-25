from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Optional: generate a key for encryption
# Save this key somewhere safe to decrypt later
key = Fernet.generate_key()
cipher = Fernet(key)

# Function to hide a message in an image
def hide_message():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG Images", "*.png"), ("BMP Images", "*.bmp")])
    if not file_path:
        return

    message = message_entry.get()
    if not message:
        messagebox.showwarning("Error", "Enter a message to hide!")
        return

    encrypt = encrypt_var.get()
    if encrypt:
        message_bytes = cipher.encrypt(message.encode())
    else:
        message_bytes = message.encode()

    message_bits = ''.join(format(byte, '08b') for byte in message_bytes)
    message_bits += '1111111111111110'  # Delimiter to mark end of message

    img = Image.open(file_path)
    img = img.convert('RGB')
    pixels = img.load()

    width, height = img.size
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= len(message_bits):
                break
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(message_bits[idx])
            idx += 1
            if idx < len(message_bits):
                g = (g & ~1) | int(message_bits[idx])
                idx += 1
            if idx < len(message_bits):
                b = (b & ~1) | int(message_bits[idx])
                idx += 1
            pixels[x, y] = (r, g, b)
        if idx >= len(message_bits):
            break

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")], title="Save Image As")
    if output_path:
        img.save(output_path)
        messagebox.showinfo("Success", f"Message hidden successfully!\nSaved as: {output_path}")

def extract_message():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("PNG Images", "*.png"), ("BMP Images", "*.bmp")]
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path)
        img = img.convert('RGB')
        pixels = img.load()

        width, height = img.size
        bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                bits.append(r & 1)
                bits.append(g & 1)
                bits.append(b & 1)

        # Convert bits into bytes
        message_bytes = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            byte_str = ''.join(map(str, byte))
            if byte_str == '11111111':  # safer end marker
                break
            message_bytes.append(int(byte_str, 2))

        if len(message_bytes) == 0:
            raise ValueError("No hidden message found.")

        encrypt = encrypt_var.get()
        if encrypt:
            message = cipher.decrypt(bytes(message_bytes)).decode()
        else:
            message = bytes(message_bytes).decode(errors='ignore')

        messagebox.showinfo("Message Extracted", f"Hidden message:\n{message}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract message!\n\n{str(e)}")


# --- GUI Setup ---
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("400x250")

# Message input
tk.Label(root, text="Enter message to hide:").pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

# Encrypt checkbox
encrypt_var = tk.BooleanVar()
tk.Checkbutton(root, text="Encrypt message", variable=encrypt_var).pack()

# Buttons
tk.Button(root, text="Hide Message in Image", command=hide_message, width=25, bg="lightgreen").pack(pady=10)
tk.Button(root, text="Extract Message from Image", command=extract_message, width=25, bg="lightblue").pack(pady=5)

root.mainloop()
