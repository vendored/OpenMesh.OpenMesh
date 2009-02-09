################################################################################
#
################################################################################

message(1)

contains( OPENFLIPPER , OpenFlipper ){
	include( $$TOPDIR/qmake/all.include )
} else {
	include( $$TOPDIR/OpenMesh/qmake/all.include )
}

INCLUDEPATH += ../../..

Application()
glew()
glut()
openmesh()

DIRECTORIES = .. ../../QtViewer

# Input
HEADERS += $$getFilesFromDir($$DIRECTORIES,*.hh)
SOURCES += $$getFilesFromDir($$DIRECTORIES,*.cc)
SOURCES -= ../decimaterviewer.cc ../../QtViewer/meshviewer.cc 
FORMS   += $$getFilesFromDir($$DIRECTORIES,*.ui)

################################################################################