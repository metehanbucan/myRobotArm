import numpy as np
import json
import asyncio
import serial
import websockets
from angle_transforms import angles_motor_transform
from dynamic import calculate_dynamics
from ik import analytic_ik
from robot_config import GList, MList, SList
from trajectory import generate_trapezoidal_trajectory


gravity_g = np.array([0, 0, 9.81])
arduino = None
current_angles = [0, 45, 0, 0]

async def robot_control_server(websocket):
    global current_angles
    try:
        async for message in websocket:
            data = json.loads(message)
            program_sequence = data.get("sequence", [])
            if not program_sequence:
                continue
            main_waypoints = []
            main_torque_list = []
            current_q = current_angles.copy()
            for step in program_sequence:
                target_q_ik = analytic_ik(step["x"]/1000, step["y"]/1000, step["z"]/1000)
                target_q = [target_q_ik[0], target_q_ik[1], target_q_ik[2], step["gripper"]]
                step_trajectory = generate_trapezoidal_trajectory(current_q, target_q, total_time=2.0)
                step_torques = calculate_dynamics(step_trajectory, 0.05, SList, MList, GList, gravity_g)
                main_waypoints.extend(step_trajectory)
                main_torque_list.extend(step_torques)
                current_q = target_q.copy()

            graphic_package = {
                "type": "batch_data",
                "total_steps": len(main_waypoints),
                "data": []
            }

            for i in range(len(main_waypoints)):
                graphic_package["data"].append({
                    "time": round(i * 0.05, 2),
                    "tau1": float(main_torque_list[i][0]), 
                    "tau2": float(main_torque_list[i][1]), 
                    "tau3": float(main_torque_list[i][2])
                })
                
            await websocket.send(json.dumps(graphic_package))

            for i, q in enumerate(main_waypoints):
                motor_commands = angles_motor_transform(q)
                for data in motor_commands:
                    mesaj_str = f"{data['motor_no']},{data['aci']}\n"
                    arduino.write(mesaj_str.encode('utf-8'))
                    arduino.reset_input_buffer()
                progress_package = {"type": "progress", "step": i}
                await websocket.send(json.dumps(progress_package))
                await asyncio.sleep(0.05)
            await websocket.send(json.dumps({"type": "completed"}))
            print("Fiziksel hareket ve veri aktarımı başarıyla tamamlandı.")
            current_angles = target_q.copy()

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")



async def main():
    global arduino
    try:
        print("Arduino'ya bağlanılıyor...")
        arduino = serial.Serial('COM11', 115200, timeout=1)
        await asyncio.sleep(2)
        print("Arduino Bağlantısı Hazır!")

        async with websockets.serve(robot_control_server, "localhost", 8765):
            print("🚀 WebSocket Sunucusu Başlatıldı! 8765 portunda dinleniyor...")
            print("React arayüzünden komut bekleniyor... (Kapatmak için Ctrl+C'ye basın)")
            await asyncio.Future() 
            
    except asyncio.exceptions.CancelledError:
        pass 
    except KeyboardInterrupt:
        print("\nKullanıcı sunucuyu durdurdu.")
    finally:
        if arduino is not None and arduino.is_open:
            arduino.close()
            print("Arduino bağlantısı güvenle kapatıldı. Görüşmek üzere!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass