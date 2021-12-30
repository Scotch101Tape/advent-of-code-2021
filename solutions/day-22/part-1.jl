# 542408 is too low
# 522181 is too low
# 577204 is wrong
# Answer is 577205

using SolidModeling

struct ReactorCube
    on::Bool
    cube
end

# Parse input
reactor_cubes = ReactorCube[]
re = r"(on|off) x=(-?\d*)\.\.(-?\d*),y=(-?\d*)\.\.(-?\d*),z=(-?\d*)\.\.(-?\d*)"
for line in readlines("input.txt")
    result = match(re, line).captures

    x_min = parse(Float64, result[2])
    y_min = parse(Float64, result[4])
    z_min = parse(Float64, result[6])
    x_max = parse(Float64, result[3])
    y_max = parse(Float64, result[5])
    z_max = parse(Float64, result[7])

    # ignore outside of -50 .. 50, -50 .. 50, -50 .. 50
    if x_min < -50.0 || x_max > 50.0 || y_min < -50.0 || y_max > 50.0 || z_min < -50.0 || z_max > 50.0
        continue
    end

    
    # Create the cube
    new_cube = cube(x_min, y_min, z_min, x_max + 1.0, y_max + 1.0, z_max + 1.0)

    new_reactor_cube = ReactorCube(
        result[1] == "on" ? true : false,
        new_cube
    )

    push!(reactor_cubes, new_reactor_cube)
end

# Combine the cubes together and get the volume
mega_cube = reduce((a, b) -> b.on ? bunion(a, b.cube) : bsubtract(a, b.cube), reactor_cubes; init = cube(0.0, 0.0, 0.0, 1.0, 1.0, 1.0))

# Print the volume
print(volume(mega_cube))

#print("\n")
#cube(10.0, 10.0, 10.0, 13.0, 13.0, 13.0) |> volume |> print