import os
from flask import render_template, request, redirect, url_for
from init import app, db
from models import Project, User, ProjectImage, SavedProject
from werkzeug.utils import secure_filename

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/gallery')
def gallery_page():
    projects = db.session.execute(db.select(Project).order_by(Project.id)).scalars()
    # projects = Project.query.all()
    return render_template('gallery.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_page(project_id):
    project = Project.query.get(project_id)
    return render_template('project.html', project=project)

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        project_name = request.form['project_name']
        text = request.form['text']
        project = Project(title=project_name, description=text)
        db.session.add(project)
        if 'images' in request.files:
            uplode_images(request, project)

        db.session.commit()

        # return redirect('/gallery')

    return render_template('upload.html')

def uplode_images(request, project):
    images = request.files.getlist('images')
    image_name = request.form['images_labels']
    print(image_name)
    if len(images) == '':
        flash('No selected file')
        return redirect(request.url)

    for i, image in enumerate(images):
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],'images', filename)
            image.save(image_path)
            project_image = ProjectImage(project=project, url=image_path)
            db.session.add(project_image)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/user/gallery')
# def user_gallery_page():
#     saved_projects = SavedProject.query.filter_by(user_id=current_user.id).all()
#     return render_template('user_gallery.html', saved_projects=saved_projects)

if __name__ == '__main__':
    app.run(debug=True)
