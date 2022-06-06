import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaltjoblistComponent } from './saltjoblist.component';

describe('SaltjoblistComponent', () => {
  let component: SaltjoblistComponent;
  let fixture: ComponentFixture<SaltjoblistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SaltjoblistComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SaltjoblistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
