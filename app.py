import streamlit as st

st.title("🔧 CNC G-Code Generator (Turning, Facing, Step Turning)")

operation = st.selectbox(
    "Do you want to do any operations other than turning and facing?",
    ["No (Only Turning and/or Facing)", "Yes (Add Step Turning)"]
)

if operation == "No (Only Turning and/or Facing)":
    st.subheader("🧾 Input: Facing and Turning Details")
    initial_dia = st.number_input("Initial Diameter of Workpiece", value=50.0)
    final_dia = st.number_input("Final Diameter of Workpiece", value=40.0)
    initial_len = st.number_input("Initial Length of Workpiece", value=100.0)
    final_len = st.number_input("Final Length of Workpiece", value=80.0)

    dia_diff = initial_dia - final_dia
    len_diff = initial_len - final_len

    if dia_diff > 0 or len_diff > 0:
        tool_number = st.text_input("Tool Number (e.g., 01)", value="01")
        offset_number = st.text_input("Offset Number (e.g., 01)", value="01")
        spindle_speed = st.text_input("Spindle Speed (RPM)", value="1200")
        feed_rate = st.text_input("Feed Rate (e.g., 0.2)", value="0.2")
        depth_of_cut_facing = st.number_input("Depth of Cut per Pass (Facing)", value=1.0, min_value=0.01, key="facing")
        depth_of_cut_turning = st.number_input("Depth of Cut per Pass (Turning)", value=1.0, min_value=0.01, key="turning")

        if st.button("🔁 Generate G-Code"):
            result = []
            if dia_diff > 0 and len_diff > 0:
                result.append(">> Perform facing followed by turning")
                # Facing
                result.append("\n>> FACING OPERATION")
                N = initial_len - final_len
                full_passes = int(N // depth_of_cut_facing)
                final_pass = N % depth_of_cut_facing
                total_cut = 0
                result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
                result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
                result.append(f"S{spindle_speed} M03 (Spindle speed and start)")
                result.append(f"G00 X{initial_dia + 4} Z{N + 4} M07 (Coolant on)")
                for _ in range(full_passes):
                    total_cut += depth_of_cut_facing
                    result.append(f"G00 Z{N - total_cut} (Move closer)")
                    result.append(f"G01 X-1 F{feed_rate} (Facing cut)")
                    result.append(f"G00 Z{N - total_cut + depth_of_cut_facing} X{initial_dia + 2} (Retract tool)")
                if final_pass > 0:
                    total_cut += final_pass
                    result.append(f"G00 Z{N - total_cut} (Final finishing pass)")
                    result.append(f"G01 X-1 F{feed_rate}")
                    result.append(f"G00 Z{N - total_cut + final_pass} X{initial_dia + 2}")
                # Turning
                result.append("\n>> TURNING OPERATION")
                N = initial_dia - final_dia
                full_passes = int(N // depth_of_cut_turning)
                final_pass = N % depth_of_cut_turning
                n = initial_dia
                p = 0
                result.append(f"G00 X{initial_dia + 4} Z3 M07 (Coolant on)")
                for _ in range(full_passes):
                    n -= depth_of_cut_turning
                    result.append(f"G00 X{n} Z0.5 (Positioning for cut)")
                    result.append(f"G01 Z-{final_len} F{feed_rate}")
                    result.append(f"G00 X{initial_dia - p} Z2 (Retract tool)")
                    p += depth_of_cut_turning
                if final_pass > 0:
                    n -= final_pass
                    result.append(f"G00 X{n} Z0.5 (Final finishing cut)")
                    result.append(f"G01 Z-{final_len} F{feed_rate}")
                    result.append(f"G00 X{n + 2} Z2 (Retract tool)")
            elif dia_diff > 0:
                result.append(">> Perform only turning")
                N = initial_dia - final_dia
                full_passes = int(N // depth_of_cut_turning)
                final_pass = N % depth_of_cut_turning
                n = initial_dia
                p = 0
                result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
                result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
                result.append(f"S{spindle_speed} M03 (Spindle start)")
                result.append(f"G00 X{initial_dia + 4} Z3 M07 (Coolant on)")
                for _ in range(full_passes):
                    n -= depth_of_cut_turning
                    result.append(f"G00 X{n} Z0.5 (Positioning for cut)")
                    result.append(f"G01 Z-{final_len} F{feed_rate}")
                    result.append(f"G00 X{initial_dia - p} Z2 (Retract tool)")
                    p += depth_of_cut_turning
                if final_pass > 0:
                    n -= final_pass
                    result.append(f"G00 X{n} Z0.5 (Final finishing cut)")
                    result.append(f"G01 Z-{final_len} F{feed_rate}")
                    result.append(f"G00 X{n + 2} Z2 (Retract tool)")
            elif len_diff > 0:
                result.append(">> Perform only facing")
                N = initial_len - final_len
                full_passes = int(N // depth_of_cut_facing)
                final_pass = N % depth_of_cut_facing
                total_cut = 0
                result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
                result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
                result.append(f"S{spindle_speed} M03 (Spindle start)")
                result.append(f"G00 X{initial_dia + 4} Z{N + 4} M07 (Coolant on)")
                for _ in range(full_passes):
                    total_cut += depth_of_cut_facing
                    result.append(f"G00 Z{N - total_cut} (Move closer)")
                    result.append(f"G01 X-1 F{feed_rate} (Facing cut)")
                    result.append(f"G00 Z{N - total_cut + depth_of_cut_facing} X{initial_dia + 2} (Retract tool)")
                if final_pass > 0:
                    total_cut += final_pass
                    result.append(f"G00 Z{N - total_cut} (Final facing pass)")
                    result.append(f"G01 X-1 F{feed_rate}")
                    result.append(f"G00 Z{N - total_cut + final_pass} X{initial_dia + 2}")
            else:
                result.append(">> No operation needed or invalid input")
            result.append("M09 (Coolant off)")
            result.append("M05 (Spindle off)")
            result.append("G28 U0 W0 (Return home)")
            result.append("M30 (End of program)")
            st.code("\n".join(result), language="text")
    else:
        st.info("No operation needed or invalid input.")

else:
    st.subheader("🧾 Input: Facing/Turning + Step Turning Details")
    # Basic turning/facing details
    tool_number = st.text_input("Tool Number (e.g., 01)", value="01")
    offset_number = st.text_input("Offset Number (e.g., 01)", value="01")
    spindle_speed = st.text_input("Spindle Speed (RPM)", value="1200")
    initial_dia = st.number_input("Initial Diameter of Workpiece", value=50.0)
    final_dia = st.number_input("Final Diameter of Workpiece", value=40.0)
    initial_len = st.number_input("Initial Length of Workpiece", value=100.0)
    final_len = st.number_input("Final Length of Workpiece", value=80.0)
    feed_rate = st.text_input("Feed Rate (e.g., 0.2)", value="0.2")
    depth_of_cut_facing = st.number_input("Depth of Cut per Pass (Facing)", value=1.0, min_value=0.01, key="facing2")
    depth_of_cut_turning = st.number_input("Depth of Cut per Pass (Turning)", value=1.0, min_value=0.01, key="turning2")

    # Step Turning
    st.markdown("---")
    st.subheader("Step Turning Details")
    step_tool_number = st.text_input("Step Turning Tool Number", value="02")
    step_offset_number = st.text_input("Step Turning Tool Offset", value="02")
    step_initial_dia = st.number_input("Step Turning Initial Diameter", value=initial_dia)
    step_workpiece_length = st.number_input("Step Turning Workpiece Length", value=initial_len)
    num_steps = st.number_input("Number of Steps", min_value=1, step=1, value=2)

    step_turning_sizes = []
    for i in range(int(num_steps)):
        st.markdown(f"### Step {i+1}")
        step_dia = st.number_input(f"Step {i+1} Diameter", key=f"step_dia_{i}")
        step_len = st.number_input(f"Step {i+1} Length", key=f"step_len_{i}")
        step_turning_sizes.append((step_dia, step_len))

    step_spindle_speed = st.text_input("Step Turning Spindle Speed (RPM)", value="1200")
    step_feed_rate = st.text_input("Step Turning Feed Rate (e.g., 0.2)", value="0.2")
    step_depth_of_cut = st.number_input("Step Turning Depth of Cut per Pass", value=1.0, min_value=0.01)

    if st.button("🔁 Generate G-Code (with Step Turning)"):
        result = []
        # Facing/Turning code (without closure)
        dia_diff = initial_dia - final_dia
        len_diff = initial_len - final_len

        if dia_diff > 0 and len_diff > 0:
            result.append(">> Perform facing followed by turning")
            # Facing
            result.append("\n>> FACING OPERATION")
            N = initial_len - final_len
            full_passes = int(N // depth_of_cut_facing)
            final_pass = N % depth_of_cut_facing
            total_cut = 0
            result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
            result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
            result.append(f"S{spindle_speed} M03 (Spindle speed and start)")
            result.append(f"G00 X{initial_dia + 4} Z{N + 4} M07 (Coolant on)")
            for _ in range(full_passes):
                total_cut += depth_of_cut_facing
                result.append(f"G00 Z{N - total_cut} (Move closer)")
                result.append(f"G01 X-1 F{feed_rate} (Facing cut)")
                result.append(f"G00 Z{N - total_cut + depth_of_cut_facing} X{initial_dia + 2} (Retract tool)")
            if final_pass > 0:
                total_cut += final_pass
                result.append(f"G00 Z{N - total_cut} (Final finishing pass)")
                result.append(f"G01 X-1 F{feed_rate}")
                result.append(f"G00 Z{N - total_cut + final_pass} X{initial_dia + 2}")
            # Turning
            result.append("\n>> TURNING OPERATION")
            N = initial_dia - final_dia
            full_passes = int(N // depth_of_cut_turning)
            final_pass = N % depth_of_cut_turning
            n = initial_dia
            p = 0
            result.append(f"G00 X{initial_dia + 4} Z3 M07 (Coolant on)")
            for _ in range(full_passes):
                n -= depth_of_cut_turning
                result.append(f"G00 X{n} Z0.5 (Positioning for cut)")
                result.append(f"G01 Z-{final_len} F{feed_rate}")
                result.append(f"G00 X{initial_dia - p} Z2 (Retract tool)")
                p += depth_of_cut_turning
            if final_pass > 0:
                n -= final_pass
                result.append(f"G00 X{n} Z0.5 (Final finishing cut)")
                result.append(f"G01 Z-{final_len} F{feed_rate}")
                result.append(f"G00 X{n + 2} Z2 (Retract tool)")
        elif dia_diff > 0:
            result.append(">> Perform only turning")
            N = initial_dia - final_dia
            full_passes = int(N // depth_of_cut_turning)
            final_pass = N % depth_of_cut_turning
            n = initial_dia
            p = 0
            result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
            result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
            result.append(f"S{spindle_speed} M03 (Spindle start)")
            result.append(f"G00 X{initial_dia + 4} Z3 M07 (Coolant on)")
            for _ in range(full_passes):
                n -= depth_of_cut_turning
                result.append(f"G00 X{n} Z0.5 (Positioning for cut)")
                result.append(f"G01 Z-{final_len} F{feed_rate}")
                result.append(f"G00 X{initial_dia - p} Z2 (Retract tool)")
                p += depth_of_cut_turning
            if final_pass > 0:
                n -= final_pass
                result.append(f"G00 X{n} Z0.5 (Final finishing cut)")
                result.append(f"G01 Z-{final_len} F{feed_rate}")
                result.append(f"G00 X{n + 2} Z2 (Retract tool)")
        elif len_diff > 0:
            result.append(">> Perform only facing")
            N = initial_len - final_len
            full_passes = int(N // depth_of_cut_facing)
            final_pass = N % depth_of_cut_facing
            total_cut = 0
            result.append("G28 U0 W0 (HOME POSITION, DEFAULT)")
            result.append(f"T{tool_number}{offset_number} (Tool and offset number)")
            result.append(f"S{spindle_speed} M03 (Spindle start)")
            result.append(f"G00 X{initial_dia + 4} Z{N + 4} M07 (Coolant on)")
            for _ in range(full_passes):
                total_cut += depth_of_cut_facing
                result.append(f"G00 Z{N - total_cut} (Move closer)")
                result.append(f"G01 X-1 F{feed_rate} (Facing cut)")
                result.append(f"G00 Z{N - total_cut + depth_of_cut_facing} X{initial_dia + 2} (Retract tool)")
            if final_pass > 0:
                total_cut += final_pass
                result.append(f"G00 Z{N - total_cut} (Final facing pass)")
                result.append(f"G01 X-1 F{feed_rate}")
                result.append(f"G00 Z{N - total_cut + final_pass} X{initial_dia + 2}")
        else:
            result.append(">> No operation needed or invalid input")

        # Step Turning G-code (unchanged)
        result.append("\n>> STEP TURNING OPERATION")
        result.append(f"T{step_tool_number}{step_offset_number}")
        result.append(f"G00 X{step_initial_dia + 4} Z2")
        step_p = 0
        for idx, (target_dia, step_length) in enumerate(step_turning_sizes):
            total_depth = step_initial_dia - target_dia
            full_passes = int(total_depth // step_depth_of_cut)
            remaining_cut = total_depth % step_depth_of_cut
            n = step_initial_dia
            for _ in range(full_passes):
                n -= step_depth_of_cut
                result.append(f"G00 X{n} Z{-1 * (step_p - 1)}")
                result.append(f"G01 Z{-1 * (step_p + step_length)} F{step_feed_rate}")
                result.append(f"G00 X{n + 2} Z{-1 * (step_p - 2)}")
            if remaining_cut > 0:
                n -= remaining_cut
                result.append(f"G00 X{n} Z{-1 * (step_p - 1)}")
                result.append(f"G01 Z{-1 * (step_p + step_length)} F{step_feed_rate}")
                result.append(f"G00 X{n + 2} Z{-1 * (step_p - 2)}")
            step_p += step_length

        # Closure
        result.append("M09 (Coolant off)")
        result.append("M05 (Spindle off)")
        result.append("G28 U0 W0 (Return home)")
        result.append("M30 (End of program)")
        st.code("\n".join(result), language="text")