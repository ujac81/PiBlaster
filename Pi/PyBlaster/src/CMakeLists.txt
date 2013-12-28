


FILE(GLOB pyfiles "${CMAKE_CURRENT_SOURCE_DIR}/*.py")

install(FILES ${pyfiles} DESTINATION "/opt/PyBlaster/python2.7"
        PERMISSIONS
        OWNER_READ OWNER_WRITE
        GROUP_READ
        WORLD_READ)
