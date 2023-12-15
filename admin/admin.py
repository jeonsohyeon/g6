from fastapi import APIRouter, Request

from common.database import db_session
from common.models import Board

from lib.common import *

router = APIRouter()
templates = AdminTemplates()

from admin.admin_config import router as admin_config_router
from admin.admin_member import router as admin_member_router
from admin.admin_board  import router as admin_board_router
from admin.admin_boardgroup import router as admin_boardgroup_router
from admin.admin_boardgroupmember import router as admin_boardgroupmember_router
from admin.admin_content import router as admin_content_router
from admin.admin_faq import router as admin_faq_router
from admin.admin_theme import router as admin_theme_router
from admin.admin_visit import router as admin_visit_router
from admin.admin_qa import router as admin_qa_router
from admin.admin_sendmail import router as admin_sendmail_router
from admin.admin_menu import router as admin_menu_router
from admin.admin_point import router as admin_point_router
from admin.admin_auth import router as admin_auth_router
from admin.admin_popular import router as admin_popular_router
from admin.admin_poll import router as admin_poll_router
from admin.admin_newwin import router as admin_newwin_router
from admin.admin_mail import router as admin_mail_router
from admin.admin_write_count import router as admin_write_count_router
from admin.admin_plugin import router as admin_plugin_router
from admin.admin_cache import router as admin_cache_router

router.include_router(admin_config_router, tags=["admin_config"])
router.include_router(admin_member_router, tags=["admin_member"])
router.include_router(admin_board_router, tags=["admin_board"])
router.include_router(admin_boardgroup_router, tags=["admin_boardgroup"])
router.include_router(admin_boardgroupmember_router, tags=["admin_boardgroupmember"])
router.include_router(admin_content_router, tags=["admin_content"])
router.include_router(admin_faq_router, tags=["admin_faq"])
router.include_router(admin_theme_router, tags=["admin_theme"])
router.include_router(admin_visit_router, tags=["admin_visit"])
router.include_router(admin_qa_router, tags=["admin_qa"])
router.include_router(admin_sendmail_router, tags=["admin_sendmail"])
router.include_router(admin_menu_router, tags=["admin_menu"])
router.include_router(admin_point_router, tags=["admin_point"])
router.include_router(admin_auth_router, tags=["admin_auth"])
router.include_router(admin_popular_router,  tags=["admin_popular"])
router.include_router(admin_poll_router,  tags=["admin_poll"])
router.include_router(admin_mail_router,  tags=["admin_mail"])
router.include_router(admin_newwin_router,  tags=["admin_newwin"])
router.include_router(admin_write_count_router,  tags=["admin_write_count"])
router.include_router(admin_plugin_router,  tags=["admin_plugin"])
router.include_router(admin_cache_router,  tags=["admin_cache"])

MAIN_MENU_KEY = "100100"


@router.get("/")
async def base(request: Request, db: db_session):
    """
    관리자 메인
    """
    request.session["menu_key"] = "100100"
    
    # 최근 게시물
    query = select(BoardNew, Board.bo_subject, Group.gr_subject, Group.gr_id)\
        .join(Board, BoardNew.bo_table == Board.bo_table)\
        .join(Group, Board.gr_id == Group.gr_id)\
        .order_by(BoardNew.bn_id.desc())\
        .limit(5)
    result = db.execute(query).all()
    
    new_rows = []
    for row in result:
        # print(dir(row[0]))
        write_model = dynamic_create_write_table(row[0].bo_table)

        comment = ""
        comment_link = ""        
        if row[0].wr_id == row[0].wr_parent:
            query = select(write_model.wr_subject, write_model.wr_name, write_model.wr_datetime)\
                .where(write_model.wr_id == row[0].wr_id)
            write = db.execute(query).first()
        else:
            comment = "댓글. "
            comment_link = "#c_" + row[0].wr_id
            
            query = select(write_model.wr_subject, write_model.wr_name, write_model.wr_datetime)\
                .where(write_model.wr_id == row[0].wr_parent)
            write = db.execute(query).first()
            
        new_rows.append({
            "gr_id": row.gr_id,
            "gr_subject": row.gr_subject,
            "bo_table": row[0].bo_table,
            "bo_subject": row.bo_subject,
            "wr_id": row[0].wr_id,
            "wr_parent": row[0].wr_parent,
            "wr_subject": write.wr_subject,
            "wr_name": write.wr_name,
            "wr_datetime": write.wr_datetime,
            "comment": comment,
            "comment_link": comment_link,
        })
                
    
    context = {
        "request": request,
        "new_rows": new_rows,
    }
    
    return templates.TemplateResponse("index.html", context)
