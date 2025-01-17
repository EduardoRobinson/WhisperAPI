import torch 

print(torch.cuda.is_available())  # Deve retornar True
print(torch.cuda.get_device_name(0))
